from vocabulary_quiz_app.quiz_logic import Word, toggle_bookmark, get_bookmarked_words


def test_toggle_bookmark_on() -> None:
    word = Word(term="apple", meaning="사과")
    assert word.bookmarked is False
    toggle_bookmark(word)
    assert word.bookmarked is True


def test_toggle_bookmark_off() -> None:
    word = Word(term="apple", meaning="사과")
    toggle_bookmark(word)
    toggle_bookmark(word)
    assert word.bookmarked is False


def test_get_bookmarked_words() -> None:
    words = [
        Word(term="apple", meaning="사과"),
        Word(term="book", meaning="책"),
        Word(term="chair", meaning="의자"),
    ]
    toggle_bookmark(words[0])
    toggle_bookmark(words[2])

    bookmarked = get_bookmarked_words(words)
    assert len(bookmarked) == 2
    assert words[0] in bookmarked
    assert words[2] in bookmarked


def test_get_bookmarked_words_empty() -> None:
    words = [Word(term="apple", meaning="사과")]
    assert get_bookmarked_words(words) == []