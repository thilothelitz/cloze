import math
from typing import Dict, List, Tuple


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

    def disambiguation_measure(self, word) -> float:
        max_prob = self._unk_probability
        for w, p in self._probabilities.items():
            if w == word:
                continue
            if p > max_prob:
                max_prob = p
        return self[word] - max_prob

    @classmethod
    @property
    def zero(cls):
        return cls({}, unk_probability=0)


class Sentence:
    def __init__(self, words: List[str], distributions: List[ProbabilityDistribution]):
        self.words = words
        self.distributions = distributions

    def __eq__(self, other: "Sentence"):
        return self.words == other.words


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
    joint_distribution = sum(
        [gap.gap_distribution for gap in bundle], start=ProbabilityDistribution.zero
    )
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
