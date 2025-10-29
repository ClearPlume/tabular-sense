from typing import Any

import torch
from torch import Tensor
from torch.nn import BCEWithLogitsLoss
from torch.utils.data import DataLoader
from tqdm import tqdm

from src.tabular_sense.components.collate import collate_fn
from src.tabular_sense.components.config import Config
from src.tabular_sense.components.dataset import ColumnDataset
from src.tabular_sense.components.metrics import MultiLabelMetrics
from src.tabular_sense.components.model import Model
from src.tabular_sense.components.sampler import LengthGroupSampler
from src.tabular_sense.components.tokenizer import Tokenizer
from src.tabular_sense.path import get_data_dir, get_models_dir


def main():
    metrics = MultiLabelMetrics()
    criterion = BCEWithLogitsLoss()
    total_loss = 0
    all_predictions: list[Tensor] = []
    all_labels: list[Tensor] = []

    tokenizer, model, test_loader = initialize("2025-10-29")
    device = next(model.parameters()).device
    progress: tqdm[dict[str, Any]] = tqdm(test_loader, f"[Test]")

    for batch in progress:
        input_ids = batch["input_ids"].to(device)
        attention_masks = batch["attention_masks"].to(device)
        labels = batch["labels"].to(device)

        with torch.no_grad():
            logits = model(input_ids, attention_masks)

        total_loss += criterion(logits, labels).item()
        probabilities = torch.sigmoid(logits)
        prediction = (probabilities > 0.5).float()
        all_predictions.append(prediction)
        all_labels.append(labels)

    avg_loss = total_loss / len(test_loader)
    score = metrics(all_predictions, all_labels).score

    print(f"loss: {avg_loss}, score: {score}")


def initialize(name: str) -> tuple[Tokenizer, Model, DataLoader[ColumnDataset]]:
    config = Config.final()

    tokenizer = Tokenizer(str(data_dir / "vocab/tabular_sense.model"))

    model = Model(tokenizer, config)
    checkpoint = torch.load(model_dir / f"checkpoint/{name}/checkpoint_{name}_best.pt")
    model.load_state_dict(checkpoint["model_state"])
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

    return tokenizer, model, test_loader


if __name__ == '__main__':
    data_dir = get_data_dir()
    model_dir = get_models_dir()
    main()
