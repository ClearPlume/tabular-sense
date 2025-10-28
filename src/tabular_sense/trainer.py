from pathlib import Path
from typing import Any

import torch
from torch import Tensor
from torch.nn import BCEWithLogitsLoss
from torch.nn.utils import clip_grad_norm_
from torch.optim import Optimizer
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm

from src.tabular_sense.components.config import Config
from src.tabular_sense.components.dropout_scheduler import DropoutScheduler
from src.tabular_sense.components.metrics import Metrics
from src.tabular_sense.components.metrics import MultiLabelMetrics
from src.tabular_sense.components.model import Model
from src.tabular_sense.components.resume_strategy import ResumeStrategy
from src.tabular_sense.path import get_models_dir, get_logs_dir


class Trainer:
    """训练器"""

    model: Model
    device: torch.device
    config: Config
    train_loader: DataLoader
    val_loader: DataLoader
    optimizer: Optimizer
    lr_scheduler: ReduceLROnPlateau
    dp_scheduler: DropoutScheduler

    early_stop_count: int
    early_stop_patience: int
    train_name: str
    start_epoch: int
    epochs: int
    criterion: BCEWithLogitsLoss
    metrics: MultiLabelMetrics
    summary: SummaryWriter
    best_score: float
    best_epoch: int
    checkpoint_dir: Path

    def __init__(
            self,
            model: Model,
            device: torch.device,
            config: Config,
            train_loader: DataLoader,
            val_loader: DataLoader,
            optimizer: Optimizer,
            lr_scheduler: ReduceLROnPlateau,
            dp_scheduler: DropoutScheduler,
            train_name: str,
            early_stop_patience: int = 6,
            epochs: int = 50,
    ):
        """
        :param train_name: 训练名称，将作为日志路径、模型保存路径的一部分
        """

        self.model = model
        self.device = device
        self.config = config
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.optimizer = optimizer
        self.lr_scheduler = lr_scheduler
        self.dp_scheduler = dp_scheduler

        self.early_stop_count = 0
        self.early_stop_patience = early_stop_patience
        self.train_name = train_name
        self.start_epoch = 1
        self.epochs = epochs
        self.criterion = BCEWithLogitsLoss()
        self.metrics = MultiLabelMetrics()
        self.summary = SummaryWriter(str(get_logs_dir() / train_name))
        self.best_score = 0
        self.best_epoch = 1
        self.checkpoint_dir = get_models_dir() / f"checkpoint/{train_name}"

        if not self.checkpoint_dir.exists():
            self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

    def load_checkpoint(
            self,
            checkpoint_name: str,
            resume_strategy: ResumeStrategy,
            reset_training_state: bool = False,
    ):
        """从存档点中恢复状态"""

        print(f"▶ 尝试加载存档点: {checkpoint_name}")
        checkpoint_path = self.checkpoint_dir / f"checkpoint_{checkpoint_name}_best.pt"

        if not checkpoint_path.exists():
            raise FileNotFoundError(f"Checkpoint file {checkpoint_path} not found")

        checkpoint = torch.load(checkpoint_path, map_location=self.device)

        self.model.load_state_dict(checkpoint["model_state"])
        print("✓ 模型权重已加载")

        if resume_strategy == ResumeStrategy.ALL_COMPONENTS:
            self.optimizer.load_state_dict(checkpoint["optimizer_state"])
            self.lr_scheduler.load_state_dict(checkpoint["lr_scheduler_state"])
            self.dp_scheduler.load_state_dict(checkpoint["dp_scheduler_state"])

            print("✓ 完全恢复：优化器 + LR调度器 + 丢弃率调度器")

        elif resume_strategy == ResumeStrategy.EXCLUDE_OPTIMIZATION:
            self.dp_scheduler.load_state_dict(checkpoint["dp_scheduler_state"])

            lr = checkpoint["optimizer_state"]["param_groups"][0]["lr"]
            for param_group in self.optimizer.param_groups:
                param_group['lr'] = lr

            print(f"✓ 部分恢复：丢弃率调度器 + checkpoint学习率")
            print(f"✗ 优化器和LR调度器使用新配置")

        elif resume_strategy == ResumeStrategy.EXCLUDE_REGULARIZATION:
            self.optimizer.load_state_dict(checkpoint["optimizer_state"])
            self.lr_scheduler.load_state_dict(checkpoint["lr_scheduler_state"])

            self.dp_scheduler.current_dropout = checkpoint["dp_scheduler_state"]["current_dropout"]
            self.dp_scheduler.train_losses = checkpoint["dp_scheduler_state"]["train_losses"]
            self.dp_scheduler.val_losses = checkpoint["dp_scheduler_state"]["val_losses"]

            print(f"✓ 部分恢复：优化器 + LR调度器")
            print(f"✗ 丢弃率调度器使用新配置，仅恢复checkpoint的dropout和历史loss")

        else:
            lr = checkpoint["optimizer_state"]["param_groups"][0]["lr"]
            for param_group in self.optimizer.param_groups:
                param_group['lr'] = lr

            self.dp_scheduler.current_dropout = checkpoint["dp_scheduler_state"]["current_dropout"]
            self.dp_scheduler.train_losses = checkpoint["dp_scheduler_state"]["train_losses"]
            self.dp_scheduler.val_losses = checkpoint["dp_scheduler_state"]["val_losses"]

            print(f"✗ 优化器、LR调度器使用新配置，仅恢复checkpoint的学习率和部分dropout状态")

        if not reset_training_state:
            self.best_score = checkpoint["best_score"]
            self.best_epoch = checkpoint["best_epoch"]
            self.early_stop_count = checkpoint["early_stop_count"]
            self.start_epoch = checkpoint["start_epoch"]

    def train(self):
        print("=" * 60)
        print("🚀 开始训练")
        print(f"    Epochs: {self.start_epoch} -> {self.epochs}")
        print(f"    模型架构: {self.config}")
        print(f"    参数规模: {self.model.param_num}")
        print(f"    当前学习率: {self.lr_scheduler.get_last_lr()[0]:.2e}")
        print(f"    当前Dropout: {self.dp_scheduler.current_dropout}")
        print(f"    最佳分数: {self.best_score}")
        print("=" * 60)

        for epoch in range(self.start_epoch, self.epochs + 1):
            train_loss = self.train_epoch(epoch)
            val_loss, metrics = self.validate_epoch(epoch)

            print(f"⏭️ Epoch {epoch}/{self.epochs}")
            print(f"    Train loss: {train_loss:.8f}")
            print(f"    Val loss: {val_loss:.8f}")
            print(f"    Score: {metrics.score:.8f}")
            print(f"    F1: {metrics.f1:.8f}")
            print(f"    LR: {self.lr_scheduler.get_last_lr()[0]:.2e}")
            print(f"    DP: {self.dp_scheduler.current_dropout}")

            old_lr = self.lr_scheduler.get_last_lr()[0]
            self.lr_scheduler.step(val_loss)
            new_lr = self.lr_scheduler.get_last_lr()[0]

            if old_lr != new_lr:
                print(f"🔄 学习率调整 ({epoch}): {old_lr:.2e} -> {new_lr:.2e}")
                self.summary.add_text("Hyperparams", f"🔄 学习率调整 ({epoch}): {old_lr:.2e} -> {new_lr:.2e}", epoch)

            old_dp = self.dp_scheduler.current_dropout
            new_dp = self.dp_scheduler.step(train_loss, val_loss)

            if old_dp != new_dp:
                self.early_stop_count = 0

                print(f"⚠️ 检测到过拟合趋势 ({epoch})")
                print(f"🔄 Epoch {epoch}: Dropout {old_dp:.3f} → {new_dp:.3f}, 早停计数重置")

                self.summary.add_text(
                    "Hyperparams",
                    f"⚠️ 检测到过拟合趋势 ({epoch})\n🔄 Epoch {epoch}: Dropout {old_dp:.3f} → {new_dp:.3f}, 早停计数重置",
                    epoch,
                )

            self.summary.add_scalars("Training/Loss", {
                "train": train_loss,
                "val": val_loss,
            }, epoch)
            self.summary.add_scalar("Training/Score", metrics.score, epoch)
            self.summary.add_scalars("Metrics", {
                "Precision": metrics.precision,
                "Recall": metrics.recall,
                "F1": metrics.f1,
            }, epoch)
            self.summary.add_scalar("Metrics/Hamming Loss", metrics.hamming_loss, epoch)
            self.summary.add_scalar("Metrics/EM", metrics.em, epoch)
            self.summary.add_scalar("Hyperparams/LR", self.lr_scheduler.get_last_lr()[0], epoch)
            self.summary.add_scalar("Hyperparams/DP", self.dp_scheduler.current_dropout, epoch)

            if self._is_best(metrics, epoch):
                print(f"✨ 新的最佳模型 (Epoch {self.best_epoch}, Score={metrics.score:.8f})")
                self.summary.add_text(
                    "BestModel",
                    f"✨ 新的最佳模型 (Epoch {self.best_epoch}, Score={metrics.score:.8f})",
                    epoch,
                )
                torch.save(
                    {
                        "model_state": self.model.state_dict(),
                        "optimizer_state": self.optimizer.state_dict(),
                        "lr_scheduler_state": self.lr_scheduler.state_dict(),
                        "dp_scheduler_state": self.dp_scheduler.state_dict(),
                        "best_score": self.best_score,
                        "best_epoch": self.best_epoch,
                        "early_stop_count": self.early_stop_count,
                        "start_epoch": epoch + 1,
                    },
                    self.checkpoint_dir / f"checkpoint_{self.train_name}_best.pt",
                )

            self.summary.add_scalars("Early Stopping", {
                "early_stop_count": self.early_stop_count,
                "early_stop_patience": self.early_stop_patience,
            }, epoch)

            if self.early_stop_count >= self.early_stop_patience:
                print(f"🚨 早停触发: 连续 {self.early_stop_patience} 个epoch无提升")
                print(f"    最佳模型: Epoch {self.best_epoch}, Score={self.best_score:.8f}")
                self.summary.add_text(
                    "EarlyStop",
                    f"🚨 早停触发: 连续 {self.early_stop_patience} 个epoch无提升\n    最佳模型: Epoch {self.best_epoch}, Score={self.best_score:.8f}",
                    epoch,
                )
                break

        self.summary.close()
        print("=" * 60)
        print("✅ 训练完成")
        print(f"    最佳分数: {self.best_score:.8f} (Epoch {self.best_epoch})")

    def train_epoch(self, epoch: int) -> float:
        self.model.train()
        total_loss = 0.0
        progress: tqdm[dict[str, Any]] = tqdm(self.train_loader, f"Epoch {epoch}/{self.epochs} [Train]")

        for idx, batch in enumerate(progress):
            logits, loss, labels = self._predict(batch)
            total_loss += loss.item()

            self.optimizer.zero_grad()
            loss.backward()

            if idx % 100 == 0:
                self._record_gradients(epoch)

            clip_grad_norm_(self.model.parameters(), self.config.max_grad_norm)
            self.optimizer.step()

            progress.set_postfix({
                "loss": f"{loss.item():.8f}",
                "lr": f"{self.lr_scheduler.get_last_lr()[0]:.2e}",
                "dp": f"{self.dp_scheduler.current_dropout}",
            })

        avg_loss = total_loss / len(self.train_loader)
        progress.set_postfix({
            "loss": f"{avg_loss:.8f}",
            "lr": f"{self.lr_scheduler.get_last_lr()[0]:.2e}",
            "dp": f"{self.dp_scheduler.current_dropout}",
        })
        return avg_loss

    @torch.no_grad()
    def validate_epoch(self, epoch: int) -> tuple[float, Metrics]:
        self.model.eval()
        total_loss = 0.0
        all_predictions: list[Tensor] = []
        all_labels: list[Tensor] = []
        progress: tqdm[dict[str, Any]] = tqdm(self.val_loader, f"Epoch {epoch}/{self.epochs} [Val]")

        for batch in progress:
            logits, loss, labels = self._predict(batch)
            total_loss += loss.item()
            probabilities = torch.sigmoid(logits)
            prediction = (probabilities > 0.5).float()

            all_predictions.append(prediction)
            all_labels.append(labels)

            progress.set_postfix({
                "loss": f"{loss.item():.8f}",
                "lr": f"{self.lr_scheduler.get_last_lr()[0]:.2e}",
                "dp": f"{self.dp_scheduler.current_dropout}",
            })

        avg_loss = total_loss / len(self.val_loader)
        progress.set_postfix({
            "loss": f"{avg_loss:.8f}",
            "lr": f"{self.lr_scheduler.get_last_lr()[0]:.2e}",
            "dp": f"{self.dp_scheduler.current_dropout}",
        })
        return avg_loss, self.metrics(all_predictions, all_labels)

    def _predict(self, batch: dict[str, Any]) -> tuple[Tensor, Tensor, Tensor]:
        """
        模型预测
        
        :return tuple[logits, loss, labels]
        """

        input_ids = batch["input_ids"].to(self.config.device)
        attention_masks = batch["attention_masks"].to(self.config.device)
        labels = batch["labels"].to(self.config.device)

        logits = self.model(input_ids, attention_masks)
        loss = self.criterion(logits, labels)
        return logits, loss, labels

    def _is_best(self, metrics: Metrics, epoch: int) -> bool:
        """判断并更新最佳记录和早停计数"""

        improvement = metrics.score - self.best_score
        if improvement > self.config.min_delta:
            if self.early_stop_count > 0:
                print(f"✔️ 早停计数重设 ({epoch})")
                self.summary.add_text("EarlyStop", f"✔️ 早停计数重设 ({epoch})", epoch)

            self.best_score = metrics.score
            self.best_epoch = epoch
            self.early_stop_count = 0

            return True
        else:
            self.early_stop_count += 1

            if self.early_stop_count < self.early_stop_patience // 2:
                symbol = "⏳"
            elif self.early_stop_count < self.early_stop_patience * 0.8:
                symbol = "⚠️"
            else:
                symbol = "🚨"

            print(f"{symbol} 接近早停阈值 ({self.early_stop_count}/{self.early_stop_patience})")
            self.summary.add_text(
                "EarlyStop",
                f"{symbol} 接近早停阈值 ({self.early_stop_count}/{self.early_stop_patience})",
                epoch,
            )
            return False

    def _record_gradients(self, epoch: int):
        """记录关键组件的梯度范数到TensorBoard"""

        def get_component_group(component: str) -> str:
            """根据参数名称确定所属组件分组"""
            if component == "cls_parameter":
                return "cls_parameter"
            elif component == "embedding.weight":
                return "embedding"
            elif component.startswith("encoder.layers.0."):
                return "encoder_first"
            elif component.startswith(f"encoder.layers.{self.config.n_encoder_layers // 2}."):
                return "encoder_mid"
            elif component.startswith(f"encoder.layers.{self.config.n_encoder_layers - 1}."):
                return "encoder_last"
            else:
                return "classifier"

        # 初始化梯度分组
        grad_groups = {}

        # 遍历所有参数，收集梯度范数
        for name, param in self.model.named_parameters():
            if param.grad is None:
                continue

            group = get_component_group(name)
            if group is None:
                continue

            grad_norm = param.grad.norm().item()
            grad_groups.setdefault(group, []).append(grad_norm)

        # 写入TensorBoard（每组取平均）
        for group, norms in grad_groups.items():
            if norms:  # 确保列表不为空
                avg_norm = sum(norms) / len(norms)
                self.summary.add_scalar(f"GradNorm/{group}", avg_norm, epoch)

        # 记录全局梯度范数（所有参数）
        total_norm = 0.0
        for p in self.model.parameters():
            if p.grad is not None:
                param_norm = p.grad.norm().item()
                total_norm += param_norm ** 2
        total_norm = total_norm ** 0.5
        self.summary.add_scalar("GradNorm/global", total_norm, epoch)
