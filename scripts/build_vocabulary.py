import random

import sentencepiece as spm

from scripts.d_model_calculator import d_model_calculator
from src.tabular_sense.core.constants import PAD_TOKEN_ID, PAD_TOKEN, VOCAB_SIZE, SEP_TOKEN, RAW_CORPUS_PER_INPUT, \
    SAMPLES_PER_TYPE, N_CLASSES
from src.tabular_sense.path import get_data_dir

data_dir = get_data_dir()
(data_dir / "vocab").mkdir(parents=True, exist_ok=True)

# 样本文件路径
samples_dir = data_dir / "samples"

if not samples_dir.exists():
    raise FileNotFoundError("Samples directory does not exist")


def train():
    sample_file = f"{samples_dir}/samples.txt"

    # TODO `―匚`训练测试
    spm.SentencePieceTrainer.Train(
        input=sample_file,
        model_prefix=f"{data_dir}/vocab/tabular_sense",
        model_type="unigram",
        vocab_size=VOCAB_SIZE,
        max_sentencepiece_length=256,
        max_sentence_length=8000,
        pad_id=PAD_TOKEN_ID,
        pad_piece=PAD_TOKEN,
        user_defined_symbols=[SEP_TOKEN],
        shuffle_input_sentence=True,
        character_coverage=0.9995,
        hard_vocab_limit=False,
        normalization_rule_name="identity",
        remove_extra_whitespaces=False,
        split_digits=True,
        add_dummy_prefix=False,
    )


def verify() -> tuple[int, float]:
    """
    Tokenizer分析
    
    :return: [vocab_size, avg_sample_length]
    """

    tokenizer = spm.SentencePieceProcessor()
    tokenizer.Load(f"{data_dir}/vocab/tabular_sense.model")

    samples_per_type = 3000
    test_cases = []

    print("loading test cases...")
    for file in samples_dir.iterdir():
        if not file.name.startswith("samples"):
            test_cases.extend(random.choices(file.read_text(encoding="utf-8").splitlines(), k=samples_per_type))
            print(f"file {file.name} loaded")
    print("test cases loaded")

    # 评估指标
    token_lengths = []
    used_token_ids = set()

    for test_case in test_cases:
        encoded = tokenizer.Encode(test_case)
        token_lengths.append(len(encoded))
        used_token_ids.update(encoded)

    # 统计分析
    vocab_size = tokenizer.vocab_size()
    avg_length = sum(token_lengths) / len(token_lengths)
    min_length = min(token_lengths)
    max_length = max(token_lengths)
    sorted_lengths = sorted(token_lengths)
    median_length = sorted_lengths[len(sorted_lengths) // 2]

    vocab_usage = len(used_token_ids) / vocab_size * 100

    # 单个数据项的 token 统计
    avg_per_item = avg_length / RAW_CORPUS_PER_INPUT
    median_per_item = median_length / RAW_CORPUS_PER_INPUT

    # 输出评估报告
    print(f"{'=' * 60}")
    print(f"词表评估报告 (VOCAB_SIZE={vocab_size})")
    print(f"{'=' * 60}")
    print(f"测试样本数: {len(test_cases)}")
    print(f"每样本数据项数: {RAW_CORPUS_PER_INPUT}")
    print(f"-" * 60)
    print(f"样本维度:")
    print(f"  平均 token 数: {avg_length:.1f}")
    print(f"  中位数 token 数: {median_length}")
    print(f"  最小 token 数: {min_length}")
    print(f"  最大 token 数: {max_length}")
    print(f"-" * 60)
    print(f"单个数据项维度:")
    print(f"  平均 token 数: {avg_per_item:.2f}")
    print(f"  中位数 token 数: {median_per_item:.2f}")
    print(f"-" * 60)
    print(f"词表使用率: {vocab_usage:.2f}% ({len(used_token_ids)}/{vocab_size})")
    print(f"{'=' * 60}")

    # 评估建议（基于单个数据项）
    if avg_per_item > 20:
        print(f"⚠️  建议: 单项平均 {avg_per_item:.1f} tokens，考虑增大词表")
    elif avg_per_item < 5:
        print(f"⚠️  建议: 单项平均 {avg_per_item:.1f} tokens，词表可能过大")
    else:
        print(f"✓ 词表大小合理 (单项平均 {avg_per_item:.1f} tokens)")

    if vocab_usage < 50:
        print(f"⚠️  建议: 词表使用率过低 ({vocab_usage:.1f}%)，可能存在大量冗余")
    elif vocab_usage > 95:
        print(f"⚠️  建议: 词表使用率过高 ({vocab_usage:.1f}%)，词表可能不够")

    return vocab_size, avg_length


def main():
    # train()
    vocab_size, sample_len = verify()
    d_model = d_model_calculator(vocab_size, N_CLASSES * SAMPLES_PER_TYPE * sample_len, 30, 1)
    print(f"推荐维度：{d_model}")


if __name__ == "__main__":
    main()
