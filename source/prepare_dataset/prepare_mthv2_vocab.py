#!/usr/bin/env python3

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Expand a PaddleOCR character dictionary with characters "
            "observed in MTHv2 training data while preserving every "
            "existing dictionary index."
        )
    )

    parser.add_argument(
        "--base-dict",
        type=Path,
        required=True,
        help="Original PaddleOCR dictionary.",
    )

    parser.add_argument(
        "--train-tsv",
        type=Path,
        required=True,
        help="MTHv2 training TSV containing a 'text' column.",
    )

    parser.add_argument(
        "--output-dict",
        type=Path,
        required=True,
        help="Output expanded dictionary.",
    )

    return parser.parse_args()


def load_dictionary(path: Path) -> list[str]:
    if not path.is_file():
        raise FileNotFoundError(path)

    chars = []

    with path.open("r", encoding="utf-8") as f:
        for raw in f:
            char = raw.rstrip("\r\n")

            if not char:
                continue

            chars.append(char)

    if len(chars) != len(set(chars)):
        raise RuntimeError(
            "Base dictionary contains duplicate entries."
        )

    return chars


def load_train_characters(path: Path) -> Counter[str]:
    import csv

    if not path.is_file():
        raise FileNotFoundError(path)

    counter = Counter()

    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(
            f,
            delimiter="\t",
        )

        if reader.fieldnames is None:
            raise RuntimeError(
                f"No TSV header found: {path}"
            )

        if "text" not in reader.fieldnames:
            raise RuntimeError(
                f"'text' column missing. "
                f"Columns: {reader.fieldnames}"
            )

        for row in reader:
            text = row.get("text", "")
            counter.update(text)

    return counter


def main():
    args = parse_args()

    base_chars = load_dictionary(
        args.base_dict
    )

    train_counts = load_train_characters(
        args.train_tsv
    )

    base_set = set(base_chars)

    missing_chars = [
        char
        for char in train_counts
        if char not in base_set
    ]

    # Deterministic ordering:
    # most frequent new characters first,
    # then Unicode code point as tie-break.
    missing_chars.sort(
        key=lambda c: (
            -train_counts[c],
            ord(c),
        )
    )

    expanded_chars = (
        base_chars
        + missing_chars
    )

    args.output_dict.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with args.output_dict.open(
        "w",
        encoding="utf-8",
        newline="\n",
    ) as f:
        for char in expanded_chars:
            f.write(char + "\n")

    print("=" * 72)
    print("B2 VOCABULARY PREPARATION")
    print("=" * 72)

    print(
        f"Base dictionary size     : "
        f"{len(base_chars)}"
    )

    print(
        f"Train unique characters  : "
        f"{len(train_counts)}"
    )

    print(
        f"New characters appended  : "
        f"{len(missing_chars)}"
    )

    print(
        f"Expanded dictionary size : "
        f"{len(expanded_chars)}"
    )

    print()
    print("Top newly added characters:")

    for char in missing_chars[:30]:
        print(
            f"  {char!r:<8} "
            f"U+{ord(char):04X} "
            f"train_freq={train_counts[char]}"
        )

    # Critical verification:
    assert (
        expanded_chars[: len(base_chars)]
        == base_chars
    )

    print()
    print(
        "[OK] All original dictionary indices "
        "were preserved."
    )

    print(
        f"[OK] Expanded dictionary written to:\n"
        f"     {args.output_dict}"
    )


if __name__ == "__main__":
    main()