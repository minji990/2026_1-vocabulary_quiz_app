import random

from vocabulary_quiz_app.quiz_logic import Word, check_answer, draw_word


def test_check_answer_normalized() -> None:
    word = Word(term="apple", meaning="사과")
    assert check_answer(word, "사과")
    assert check_answer(word, "  사과 ")
    assert not check_answer(word, "apple")


def test_draw_word_uses_rng_choice() -> None:
    words = [Word(term="a", meaning="A"), Word(term="b", meaning="B")]

    class FixedRng:
        def choice(self, seq):
            return seq[0]

    assert draw_word(words, FixedRng()) == words[0]


def test_draw_word_empty_list_raises() -> None:
    try:
        draw_word([], random.Random())
    except ValueError as exc:
        assert "empty" in str(exc)
    else:
        raise AssertionError("Expected ValueError for empty word list")

#퀴즈 셔플 로직 테스트 추가
from vocabulary_quiz_app.quiz_logic import get_shuffled_words


def test_get_shuffled_words_contains_all() -> None:
    """셔플 후 모든 단어가 포함되는지 확인"""
    words = [
        Word(term="apple", meaning="사과"),
        Word(term="book", meaning="책"),
        Word(term="chair", meaning="의자"),
    ]
    shuffled = get_shuffled_words(words)
    assert len(shuffled) == len(words)
    assert set(w.term for w in shuffled) == set(w.term for w in words)


def test_get_shuffled_words_does_not_modify_original() -> None:
    """원본 리스트가 변경되지 않는지 확인"""
    words = [
        Word(term="apple", meaning="사과"),
        Word(term="book", meaning="책"),
        Word(term="chair", meaning="의자"),
    ]
    original_order = [w.term for w in words]
    get_shuffled_words(words)
    assert [w.term for w in words] == original_order