from torch.optim import AdamW
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.utils.data import DataLoader

from src.tabular_sense.components.collate import collate_fn
from src.tabular_sense.components.config import Config
from src.tabular_sense.components.dataset import ColumnDataset
from src.tabular_sense.components.dropout_scheduler import DropoutScheduler
from src.tabular_sense.components.model import Model
from src.tabular_sense.components.resume_strategy import ResumeStrategy
from src.tabular_sense.components.sampler import LengthGroupSampler
from src.tabular_sense.components.tokenizer import Tokenizer
from src.tabular_sense.path import get_data_dir
from src.tabular_sense.trainer import Trainer


def main():
    data_dir = get_data_dir()
    config = Config.final()
    tokenizer = Tokenizer(str((data_dir / "vocab/tabular_sense.model")))

    dataset = ColumnDataset(data_dir / "samples/samples.txt", tokenizer, config)
    train_dataset, val_dataset, _ = dataset.split()

    train_loader = DataLoader(
        dataset=train_dataset,
        collate_fn=collate_fn,
        batch_sampler=LengthGroupSampler("train", train_dataset, config.batch_size, True),
        num_workers=4,
        pin_memory=True,
    )
    val_loader = DataLoader(
        dataset=val_dataset,
        collate_fn=collate_fn,
        batch_sampler=LengthGroupSampler("val", val_dataset, config.batch_size, True),
        num_workers=4,
        pin_memory=True,
    )

    model = Model(tokenizer, config)

    optimizer = AdamW(
        model.parameters(),
        lr=config.learning_rate,
        betas=(0.9, 0.98),
        weight_decay=0.01
    )

    lr_scheduler = ReduceLROnPlateau(
        optimizer,
        mode='min',
        factor=0.9,
        patience=3,
    )

    dp_scheduler = DropoutScheduler(
        model.named_modules(),
        config.dropout,
        0.3,
        config.max_dropout,
        2,
    )

    trainer = Trainer(
        model=model,
        device=config.device,
        config=config,
        train_loader=train_loader,
        val_loader=val_loader,
        optimizer=optimizer,
        lr_scheduler=lr_scheduler,
        dp_scheduler=dp_scheduler,
        train_name="2025-10-30",
    )

    trainer.load_checkpoint("2025-10-30", ResumeStrategy.ALL_COMPONENTS)

    trainer.train()


if __name__ == '__main__':
    main()
