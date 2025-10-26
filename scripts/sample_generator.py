import os
import random
import shutil

from scripts.sample_utils import load_corpus
from src.tabular_sense.core.constants import CORPUS_TYPES, SAMPLES_PER_TYPE, RAW_CORPUS_PER_INPUT, \
    MAGIC_COLUMN_NAMES, GENERIC_COLUMN_NAMES, SEED_TYPES, VARIANT_TYPES, RAW_CORPUS_PER_TYPE
from src.tabular_sense.core.type_rule import infer_possible_types
from src.tabular_sense.path import get_data_dir


# 样本文件结构为：可能类型,可能类型|列名|数据<sep>数据<sep>数据
def main():
    sample_dir = get_data_dir() / "samples"
    corpus_dir = get_data_dir() / "corpus"

    if sample_dir.exists():
        shutil.rmtree(sample_dir)

    sample_dir.mkdir(parents=True, exist_ok=True)

    for corpus_type, generator in CORPUS_TYPES.items():
        if (corpus_dir / f"{corpus_type}.txt").exists():
            print(f"Corpus of {corpus_type} already exists, using it")
        else:
            print("Generating corpus for {}".format(corpus_type))
            generator(RAW_CORPUS_PER_TYPE)
            print("Corpus generated")

        sample_file = sample_dir / f"{corpus_type}.txt"
        print(f"Constructing corpus type: {sample_file}")

        with load_corpus(corpus_type) as corpus:
            print(f"Loading {corpus_type} samples...")

            samples = []
            for i in range(SAMPLES_PER_TYPE):
                if random.random() > 0.3:
                    type_name = random.choice(MAGIC_COLUMN_NAMES[corpus_type])
                else:
                    type_name = random.choice(GENERIC_COLUMN_NAMES)

                inputs = random.sample(corpus, RAW_CORPUS_PER_INPUT)
                sample = f"{corpus_type.upper()}|{type_name}|{'<sep>'.join(inputs)}"
                samples.append(sample)

                if i % 1000 == 0:
                    print(f"Generated {i} samples for {corpus_type}")

            print(f"Writing {sample_file}")
            with open(sample_file, "w", encoding="utf-8") as f:
                f.write("\n".join(samples))

        print(f"Wrote {len(samples)} samples to {sample_file}")

    for seed_type, generator in SEED_TYPES.items():
        sample_file = sample_dir / f"{seed_type}.txt"
        print(f"Constructing seed type: {sample_file}")

        samples = []
        for i in range(SAMPLES_PER_TYPE):
            if random.random() > 0.3:
                type_name = random.choice(MAGIC_COLUMN_NAMES[seed_type])
            else:
                type_name = random.choice(GENERIC_COLUMN_NAMES)

            inputs = generator(RAW_CORPUS_PER_INPUT)
            sample = f"{seed_type.upper()}|{type_name}|{'<sep>'.join(inputs)}"
            samples.append(sample)

            if i % 1000 == 0:
                print(f"Generated {i} samples for {seed_type}")

        print(f"Writing {sample_file}")
        with open(sample_file, "w", encoding="utf-8") as f:
            f.write("\n".join(samples))

        print(f"Wrote {len(samples)} samples to {sample_file}")

    for vocab_type, generator in VARIANT_TYPES.items():
        sample_file = sample_dir / f"{vocab_type}.txt"
        print(f"Constructing vocab type: {sample_file}")

        samples = []
        for i in range(SAMPLES_PER_TYPE):
            sample: str
            inputs = generator(RAW_CORPUS_PER_INPUT)
            data = "<sep>".join(inputs)

            if random.random() > 0.3:
                type_name = random.choice(GENERIC_COLUMN_NAMES)
                types = ",".join(set(infer_possible_types(inputs) + [vocab_type.upper()]))
                sample = f"{types}|{type_name}|{data}"
            else:
                type_name = random.choice(MAGIC_COLUMN_NAMES[vocab_type])
                sample = f"{vocab_type.upper()}|{type_name}|{data}"

            samples.append(sample)

            if i % 1000 == 0:
                print(f"Generated {i} samples for {vocab_type}")

        print(f"Writing {sample_file}")
        with open(sample_file, "w", encoding="utf-8") as f:
            f.write("\n".join(samples))

        print(f"Wrote {len(samples)} samples to {sample_file}")

    samples_dir = get_data_dir() / "samples"
    sample_file = f"{samples_dir}/samples.txt"

    print("Constructing samples file")
    if os.path.exists(sample_file):
        print(f"{sample_file} already exists, removing it")
        os.remove(sample_file)

    for file in samples_dir.iterdir():
        with open(sample_file, "a", encoding="utf-8") as f:
            f.write(file.read_text(encoding="utf-8"))
            f.write("\n")

    print("Samples written to {}".format(sample_file))


if __name__ == '__main__':
    main()
