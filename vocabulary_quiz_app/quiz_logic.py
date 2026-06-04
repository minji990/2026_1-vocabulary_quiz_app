from __future__ import annotations

import random

from dataclasses import dataclass, field


@dataclass
class Word:
    term: str
    meaning: str
    bookmarked: bool = field(default=False) 


def normalize_answer(text: str) -> str:
    return " ".join(text.strip().lower().split())


def check_answer(word: Word, user_input: str) -> bool:
    return normalize_answer(user_input) == normalize_answer(word.meaning)


def draw_word(words: list[Word], rng: random.Random | None = None) -> Word:
    if not words:
        raise ValueError("Word list is empty")
    chooser = rng if rng is not None else random
    return chooser.choice(words)


def toggle_bookmark(word: Word) -> None:
    """단어의 북마크 상태를 토글"""
    word.bookmarked = not word.bookmarked


def get_bookmarked_words(words: list[Word]) -> list[Word]:
    """북마크된 단어 목록 반환"""
    return [word for word in words if word.bookmarked]