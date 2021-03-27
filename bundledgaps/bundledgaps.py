import math
from typing import Dict, Iterator, List, Tuple


class ProbabilityDistribution:
    def __init__(
        self,
        probabilities: Dict[str, float],
        unk_probability: float = -math.inf,
    ):
        self._probabilities = probabilities
        self._unk_probability = unk_probability

    def __add__(self, other: "ProbabilityDistribution"):
        return ProbabilityDistribution(
            {
                word: self[word] + other[word]
                for word in set(list(self._probabilities) + list(other._probabilities))
            }
        )

    def __getitem__(self, word: str):
        return self._probabilities.get(word, self._unk_probability)

    def __iter__(self) -> Iterator[Tuple[str, float]]:
        yield from self._probabilities.items()

    def disambiguation_measure(self, word) -> float:
        max_prob = self._unk_probability
        for w, p in self._probabilities.items():
            if w == word:
                continue
            if p > max_prob:
                max_prob = p
        return self[word] - max_prob

    @classmethod
    def zero(cls):
        return cls({}, unk_probability=0)


class Sentence:
    def __init__(self, words: List[str], distributions: List[ProbabilityDistribution]):
        self.words = tuple(words)
        self.distributions = distributions

    def __str__(self) -> str:
        return " ".join(self.words)

    def __eq__(self, other: "Sentence") -> bool:
        return self.words == other.words

    def __hash__(self) -> int:
        return hash(self.words)

    def __iter__(self) -> Iterator[str]:
        yield from self.words

    def __contains__(self, word: str) -> bool:
        return word in self.words

    def gapify(self, word: str) -> "Gap":
        index = self.words.index(word)
        return Gap(self, index)

    def to_fastsubs(self) -> str:
        return '\n'.join(
            word + '\t' + '\t'.join(
                f'{subword} {probability}'
                for subword, probability in distribution
            )
            for word, distribution in zip(self.words, self.distributions)
        ) + '\n</s>\n'


class Gap:
    def __init__(self, sentence: Sentence, index: int):
        self.sentence = sentence
        self.index = index

    def __str__(self):
        return " ".join(
            word if i != self.index else "___"
            for i, word in enumerate(self.sentence.words)
        )

    @property
    def gap_distribution(self):
        return self.sentence.distributions[self.index]

    @property
    def gap_word(self):
        return self.sentence.words[self.index]


def joint_disambiguation_measure(bundle: List[Gap]):
    if len(bundle) == 0:
        raise ValueError("Bundle must contain at least one seed sentence")
    gap_word = bundle[0].gap_word
    if not all(gap.gap_word == gap_word for gap in bundle):
        raise ValueError("All gaps in a bundle must have the same gap word")
    joint_distribution = ProbabilityDistribution.zero()
    for gap in bundle:
        joint_distribution += gap.gap_distribution
    return joint_distribution.disambiguation_measure(gap_word)


def next_best_gap(bundle: List[Gap], corpus: List[Sentence]) -> Tuple[Gap, float]:
    gap_word = bundle[0].gap_word
    max_disambiguation = -math.inf
    best_gap = None
    for sentence in corpus:
        if any(gap.sentence == sentence for gap in bundle):
            continue
        index = sentence.words.index(gap_word)
        if index != -1:
            gap = Gap(sentence, index)
            disambiguation = joint_disambiguation_measure(bundle + [gap])
            if disambiguation > max_disambiguation:
                max_disambiguation = disambiguation
                best_gap = gap
    return best_gap, max_disambiguation
