import argparse
import random
from collections import defaultdict
from contextlib import ExitStack
from typing import Dict, Iterator, List, Set, TextIO

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


def extract_corpora(fastsub_file: TextIO, words: List[str]):
    with ExitStack() as stack:
        files = [
            stack.enter_context(
                open(f"{fastsub_file.name}.{word}", "w", encoding="utf-8")
            )
            for word in words
        ]
        for sentence in parse_sentences(fastsub_file):
            for i, word in enumerate(words):
                if word in sentence:
                    files[i].write(sentence.to_fastsubs())


def generate_bundles(file: TextIO, word: str, bundle_size: int):
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
    for gap, disambiguation in zip(bundle, disambiguations):
        print(gap, disambiguation)


def get_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate_parser = subparsers.add_parser("extract_corpora")
    generate_parser.add_argument("file", type=argparse.FileType("r", encoding="utf-8"))
    generate_parser.add_argument("--words", "-w", nargs="*")

    generate_parser = subparsers.add_parser("generate_bundles")
    generate_parser.add_argument("file", type=argparse.FileType("r", encoding="utf-8"))
    generate_parser.add_argument("--word", "-w", required=True)
    generate_parser.add_argument("--bundle-size", "-n", type=int, required=True)

    return parser


if __name__ == "__main__":
    parser = get_argument_parser()
    args = parser.parse_args()
    if args.command == "extract_corpora":
        extract_corpora(args.file, args.words)
    if args.command == "generate_bundles":
        generate_bundles(args.file, args.word, args.bundle_size)
