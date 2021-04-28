import argparse
import json
import math
import random
import sys
from collections import defaultdict
from contextlib import ExitStack
from typing import Dict, Iterator, List, Optional, Set, TextIO

from bundledgaps import (
    ProbabilityDistribution,
    Sentence,
    joint_disambiguation_measure,
    next_best_gap,
)


def parse_sentences(file: TextIO) -> Iterator[Sentence]:
    words = []
    distributions = []
    for line in file:
        line = line.strip()
        probabilities = {}
        word, *fillers = line.split("\t")
        if word == "</s>":
            yield Sentence(words, distributions)
            words = []
            distributions = []
            continue
        else:
            words.append(word)
        for filler in fillers:
            word, prob = filler.split(" ")
            probabilities[word] = float(prob)
        distributions.append(ProbabilityDistribution(probabilities))


def load_corpus(file: TextIO) -> Dict[str, Set[Sentence]]:
    corpus = defaultdict(set)
    for sentence in parse_sentences(file):
        for word in sentence:
            corpus[word].add(sentence)
    return corpus


def extract_corpora(
    *,
    fastsub_file: TextIO,
    words: List[str],
    preferred_vocabulary: List[str],
    min_vocabulary_ratio: float,
    max_sentence_length: int,
    max_sentences: int,
    outfile_prefix: Optional[str],
):
    with ExitStack() as stack:
        files = [
            stack.enter_context(
                open(
                    f"{outfile_prefix or fastsub_file.name}.{word}",
                    "w",
                    encoding="utf-8",
                )
            )
            for word in words
        ]
        counts = {word: 0 for word in words}
        for sentence in parse_sentences(fastsub_file):
            if (
                max_sentence_length is not None
                and len(sentence.words) > max_sentence_length
            ):
                continue

            if (
                preferred_vocabulary is not None
                and sentence.get_vocabulary_ratio(preferred_vocabulary)
                < min_vocabulary_ratio
            ):
                continue

            for i, word in enumerate(words):
                if counts[word] >= max_sentences:
                    continue
                if word in sentence:
                    files[i].write(sentence.to_fastsubs())
                    counts[word] += 1


def generate_bundles(
    *,
    file: TextIO,
    word: str,
    bundle_size: int,
):
    corpus = load_corpus(file)
    sentences = list(corpus[word])
    if len(sentences) < bundle_size:
        raise RuntimeError(f"Only {len(sentences)} sentences for '{word}'")
    random.shuffle(list(sentences))
    seed_gap = sentences.pop().gapify(word)
    bundle = [seed_gap]
    disambiguations = [joint_disambiguation_measure(bundle)]
    for _ in range(bundle_size - 1):
        next_gap, disambiguation = next_best_gap(bundle, sentences)
        bundle.append(next_gap)
        disambiguations.append(disambiguation)
    # for gap, disambiguation in zip(bundle, disambiguations):
    #     print(gap, disambiguation)
    data = {
        "target": word,
    }
    for i, gap in enumerate(bundle):
        data[f"sent_{i + 1}_left"] = gap.part_before
        data[f"sent_{i + 1}_right"] = gap.part_after
    print(json.dumps(data))


def get_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate_parser = subparsers.add_parser("extract_corpora")
    generate_parser.add_argument(
        "file",
        type=argparse.FileType("r", encoding="utf-8"),
        nargs="?",
        default=sys.stdin,
    )
    generate_parser.add_argument("--words", "-w", nargs="*")
    generate_parser.add_argument(
        "--preferred-vocabulary",
        "-v",
        type=argparse.FileType("r", encoding="utf-8"),
    )
    generate_parser.add_argument(
        "--min-vocabulary-ratio",
        "-r",
        type=float,
        default=0.8,
    )
    generate_parser.add_argument(
        "--max-sentence-length",
        "-l",
        type=int,
    )
    generate_parser.add_argument("--max-sentences", "-s", type=int, default=math.inf)
    generate_parser.add_argument("--outfile-prefix", "-o")

    generate_parser = subparsers.add_parser("generate_bundles")
    generate_parser.add_argument(
        "file",
        type=argparse.FileType("r", encoding="utf-8"),
        nargs="?",
        default=sys.stdin,
    )
    generate_parser.add_argument("--word", "-w", required=True)
    generate_parser.add_argument("--bundle-size", "-n", type=int, required=True)

    return parser


if __name__ == "__main__":
    parser = get_argument_parser()
    args = parser.parse_args()
    if args.command == "extract_corpora":
        preferred_vocabulary = None
        if args.preferred_vocabulary is not None:
            preferred_vocabulary = [
                line.strip() for line in args.preferred_vocabulary if line.strip()
            ]
        extract_corpora(
            fastsub_file=args.file,
            words=args.words,
            preferred_vocabulary=preferred_vocabulary,
            min_vocabulary_ratio=args.min_vocabulary_ratio,
            max_sentence_length=args.max_sentence_length,
            max_sentences=args.max_sentences,
            outfile_prefix=args.outfile_prefix,
        )
    if args.command == "generate_bundles":
        generate_bundles(
            file=args.file,
            word=args.word,
            bundle_size=args.bundle_size,
        )
