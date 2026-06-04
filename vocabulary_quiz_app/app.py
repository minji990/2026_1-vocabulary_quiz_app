from __future__ import annotations

import random
import tkinter as tk

from tkinter import ttk, font

from vocabulary_quiz_app.quiz_logic import (
    Word,
    check_answer,
    draw_word,
    toggle_bookmark,
    get_bookmarked_words,
)


class VocabularyQuizApp:
    def __init__(self, root: tk.Tk, words: list[Word]) -> None:
        self.words = words
        self.rng = random.Random()
        self.current: Word | None = None
        self.checked = False
        self.score = 0
        self.total = 0

        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(family="NanumGothic", size=12)

        root.title("Vocabulary Quiz")
        root.geometry("420x340")
        root.resizable(False, False)

        self.word_var = tk.StringVar(value="단어를 불러오는 중...")
        self.feedback_var = tk.StringVar(value="")
        self.score_var = tk.StringVar(value="Score: 0/0")
        self.bookmark_var = tk.StringVar(value="☆ 북마크")

        ttk.Label(root, text="영단어").pack(pady=(16, 4))
        ttk.Label(root, textvariable=self.word_var, font=("NanumGothic", 24)).pack()

        self.answer_entry = ttk.Entry(root, font=("NanumGothic", 14))
        self.answer_entry.pack(pady=12, ipadx=6, ipady=4)

        buttons = ttk.Frame(root)
        buttons.pack(pady=6)
        self.check_button = ttk.Button(buttons, text="채점", command=self.check_current)
        self.check_button.pack(side=tk.LEFT, padx=6)
        ttk.Button(buttons, text="다음", command=self.next_word).pack(
            side=tk.LEFT, padx=6
        )
        self.bookmark_button = ttk.Button(
            buttons, textvariable=self.bookmark_var, command=self.toggle_current_bookmark
        )
        self.bookmark_button.pack(side=tk.LEFT, padx=6)

        ttk.Button(root, text="북마크 단어만 보기", command=self.show_bookmarks).pack(
            pady=4
        )

        ttk.Label(root, textvariable=self.feedback_var).pack(pady=8)
        ttk.Label(root, textvariable=self.score_var).pack()

        self.next_word()

    def next_word(self) -> None:
        self.current = draw_word(self.words, self.rng)
        self.word_var.set(self.current.term)
        self.answer_entry.delete(0, tk.END)
        self.feedback_var.set("")
        self.checked = False
        self.check_button.state(["!disabled"])
        self.answer_entry.focus()
        self._update_bookmark_button()

    def check_current(self) -> None:
        if self.current is None or self.checked:
            return
        self.checked = True
        self.total += 1
        user_input = self.answer_entry.get()
        if check_answer(self.current, user_input):
            self.score += 1
            self.feedback_var.set("정답입니다!")
        else:
            self.feedback_var.set(f"오답입니다. 정답: {self.current.meaning}")
        self.score_var.set(f"Score: {self.score}/{self.total}")
        self.check_button.state(["disabled"])

    def toggle_current_bookmark(self) -> None:
        if self.current is None:
            return
        toggle_bookmark(self.current)
        self._update_bookmark_button()

    def _update_bookmark_button(self) -> None:
        if self.current is not None and self.current.bookmarked:
            self.bookmark_var.set("★ 북마크")
        else:
            self.bookmark_var.set("☆ 북마크")

    def show_bookmarks(self) -> None:
        bookmarked = get_bookmarked_words(self.words)

        popup = tk.Toplevel()
        popup.title("북마크 단어 목록")
        popup.geometry("300x300")
        popup.resizable(False, False)

        ttk.Label(popup, text=f"북마크된 단어 ({len(bookmarked)}개)").pack(pady=(12, 4))

        frame = ttk.Frame(popup)
        frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=4)

        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, font=("NanumGothic", 11))
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

        if bookmarked:
            for word in bookmarked:
                listbox.insert(tk.END, f"{word.term}  →  {word.meaning}")
        else:
            listbox.insert(tk.END, "북마크된 단어가 없습니다.")

        ttk.Button(popup, text="닫기", command=popup.destroy).pack(pady=8)