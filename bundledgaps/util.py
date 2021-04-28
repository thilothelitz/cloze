from typing import List


def detokenize(words: List[str]):
    detokenized = ""
    for i, word in enumerate(words):
        if i > 0 and not any(
            word.startswith(punct) for punct in [".", ",", ";", ":", "!", "?", "'"]
        ):
            detokenized += " "
        detokenized += word
    return detokenized
