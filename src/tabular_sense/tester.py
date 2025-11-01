import torch
from torch import Tensor
from torch.nn import BCEWithLogitsLoss
from torch.utils.data import DataLoader
from tqdm import tqdm

from src.tabular_sense.components.collate import collate_fn
from src.tabular_sense.components.config import Config
from src.tabular_sense.components.dataset import ColumnDataset, BatchedColumnSample
from src.tabular_sense.components.logger import setup_logger
from src.tabular_sense.components.metrics import MultiLabelMetrics
from src.tabular_sense.components.model import Model
from src.tabular_sense.components.sampler import LengthGroupSampler
from src.tabular_sense.components.tokenizer import Tokenizer
from src.tabular_sense.core.enum_util import ColumnType
from src.tabular_sense.path import get_data_dir, get_models_dir


def run_test(
        model: Model,
        test_loader: DataLoader[ColumnDataset],
        criterion: BCEWithLogitsLoss,
) -> tuple[float, list[Tensor], list[Tensor]]:
    """核心测试逻辑：运行模型推理并收集结果

    Args:
        model: 待测试的模型
        test_loader: 测试数据加载器
        criterion: 损失函数

    Returns:
        (平均损失, 预测结果列表, 真实标签列表)
    """
    device = next(model.parameters()).device
    total_loss = 0
    all_predictions: list[Tensor] = []
    all_labels: list[Tensor] = []

    progress: tqdm[BatchedColumnSample] = tqdm(test_loader, "[Test]")

    for batch in progress:
        input_ids = batch.input_ids.to(device)
        attention_masks = batch.attention_masks.to(device)
        labels = batch.labels.to(device)

        with torch.no_grad():
            logits = model(input_ids, attention_masks)

        total_loss += criterion(logits, labels).item()
        probabilities = torch.sigmoid(logits)
        prediction = (probabilities > 0.5).float()
        all_predictions.append(prediction)
        all_labels.append(labels)

    avg_loss = total_loss / len(test_loader)
    return avg_loss, all_predictions, all_labels


def batch_test(name: str):
    """批量测试模式：在测试集上评估模型"""
    logger = setup_logger(name, "test")
    metrics = MultiLabelMetrics()
    criterion = BCEWithLogitsLoss()

    model, test_loader, config = initialize(name)

    logger.info("=" * 60)
    logger.info("🧪 开始测试")
    logger.info(f"    Checkpoint: {name}")
    logger.info(f"    模型架构: {config.d_model}d×{config.n_head}h×{config.n_encoder_layers}L")
    logger.info(f"    参数规模: {model.param_num}")
    logger.info(f"    测试样本: {len(test_loader) * config.batch_size}")
    logger.info(f"    批次大小: {config.batch_size}")
    logger.info("=" * 60)

    avg_loss, all_predictions, all_labels = run_test(model, test_loader, criterion)
    result = metrics(all_predictions, all_labels)

    logger.info("=" * 60)
    logger.info("📊 测试结果")
    logger.info(f"    Loss: {avg_loss:.8f}")
    logger.info(f"    Score: {result.score:.8f}")
    logger.info(f"    F1: {result.f1:.8f}")
    logger.info(f"    Precision: {result.precision:.8f}")
    logger.info(f"    Recall: {result.recall:.8f}")
    logger.info(f"    Hamming Loss: {result.hamming_loss:.8f}")
    logger.info(f"    EM: {result.em:.8f}")
    logger.info("=" * 60)


def interactive_test(name: str):
    """交互测试模式：支持单样本实时预测"""
    config = Config.final()
    tokenizer = Tokenizer()

    model = Model(tokenizer.vocab_size, config)
    model.load(name)
    model.eval()

    device = next(model.parameters()).device

    print("=" * 60)
    print("🎯 交互测试模式")
    print(f"    Checkpoint: {name}")
    print(f"    模型架构: {config.d_model}d×{config.n_head}h×{config.n_encoder_layers}L")
    print(f"    参数规模: {model.param_num}")
    print("=" * 60)
    print("输入数据进行预测 (输入 'quit' 退出):")

    while True:
        data = input("\n数据> ").strip()

        if data.lower() in ["quit", "exit", "q"]:
            print("退出交互测试")
            break

        if not data:
            continue

        # Tokenize
        tokens = tokenizer.encode(data)[:config.max_len]
        input_ids = torch.tensor(tokens).unsqueeze(0).to(device)
        attention_mask = torch.ones(len(tokens)).unsqueeze(0).to(device)

        # 推理
        with torch.no_grad():
            logits = model(input_ids, attention_mask)

        probabilities = torch.sigmoid(logits)
        column_types = list(ColumnType)
        type_probabilities = {column_type.name: float(probabilities[0][idx]) for idx, column_type in
                              enumerate(column_types)}
        result = dict(sorted(type_probabilities.items(), key=lambda x: x[1], reverse=True)[:5])

        # 输出结果
        print(result)


def initialize(name: str) -> tuple[Model, DataLoader[ColumnDataset], Config]:
    config = Config.final()
    tokenizer = Tokenizer()

    model = Model(tokenizer.vocab_size, config)
    model.load(name)
    model.eval()

    dataset = ColumnDataset(data_dir / "samples/samples.txt", tokenizer, config)
    _, _, test_dataset = dataset.split()
    test_loader = DataLoader(
        dataset=test_dataset,
        collate_fn=collate_fn,
        batch_sampler=LengthGroupSampler("test", test_dataset, config.batch_size, True),
        num_workers=4,
        pin_memory=True,
    )

    return model, test_loader, config


def main():
    """主入口：支持多种测试模式"""
    import sys

    mode = sys.argv[1] if len(sys.argv) > 1 else "batch"
    name = sys.argv[2] if len(sys.argv) > 2 else "2025-10-30"

    if mode == "interactive":
        interactive_test(name)
    else:
        batch_test(name)


if __name__ == '__main__':
    data_dir = get_data_dir()
    model_dir = get_models_dir()
    main()
