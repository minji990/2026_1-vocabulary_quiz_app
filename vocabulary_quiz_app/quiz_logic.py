from __future__ import annotations

import random

from dataclasses import dataclass


@dataclass(frozen=True)
class Word:
    term: str
    meaning: str


def normalize_answer(text: str) -> str:
    return " ".join(text.strip().lower().split())


def check_answer(word: Word, user_input: str) -> bool:
    return normalize_answer(user_input) == normalize_answer(word.meaning)


def draw_word(words: list[Word], rng: random.Random | None = None) -> Word:
    if not words:
        raise ValueError("Word list is empty")
    chooser = rng if rng is not None else random
    return chooser.choice(words)

#퀴즈 셔플 로직 추가
def get_shuffled_words(words: list[Word], rng: random.Random | None = None) -> list[Word]:
    """단어 목록을 랜덤 셔플한 새 리스트 """
    chooser = rng if rng is not None else random
    shuffled = list(words)
    chooser.shuffle(shuffled)
    return shuffled