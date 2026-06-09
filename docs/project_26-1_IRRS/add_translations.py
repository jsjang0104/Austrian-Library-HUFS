"""
Qwen2.5-14B (Ollama)로 기존 도서 전체의 제목/저자 번역을 일괄 생성한다.
- 한국어(KR) 도서 → 독일어 번역 (translated_title, translated_author)
- 독일어/영어/기타(DE/EN/ETC) 도서 → 한국어 번역

실행:
  cd /home/hufs/Workspace/Austrian-Library-HUFS
  python docs/project_26-1_IRRS/add_translations.py

실행 후 build_faiss_local.py 로 FAISS 인덱스 재빌드 필요.
"""

import os
import sys

BACKEND_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "backend")
)
sys.path.insert(0, BACKEND_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

import requests
from library.models import Book

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5:14b"
TIMEOUT = 60

PROMPT_TO_KR = (
    "Translate the following book title and author from German (or English) to Korean. "
    "Reply with ONLY the translated title on line 1 and translated author on line 2. "
    "No explanations.\n"
    "Title: {title}\n"
    "Author: {author}"
)

PROMPT_TO_DE = (
    "Translate the following book title and author from Korean to German. "
    "Reply with ONLY the translated title on line 1 and translated author on line 2. "
    "No explanations.\n"
    "제목: {title}\n"
    "저자: {author}"
)


def check_ollama():
    try:
        requests.get("http://localhost:11434", timeout=5).raise_for_status()
    except Exception as exc:
        print(f"[오류] Ollama 연결 실패: {exc}")
        sys.exit(1)


def translate(title: str, author: str, to_korean: bool) -> tuple[str, str]:
    prompt_tmpl = PROMPT_TO_KR if to_korean else PROMPT_TO_DE
    prompt = prompt_tmpl.format(title=title, author=author or "")
    resp = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
        },
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    lines = [l.strip() for l in resp.json()["message"]["content"].strip().splitlines() if l.strip()]
    translated_title = lines[0] if len(lines) > 0 else ""
    translated_author = lines[1] if len(lines) > 1 else ""
    return translated_title, translated_author


def main():
    check_ollama()

    books = list(
        Book.objects.filter(translated_title__isnull=True).order_by("book_id")
    )
    total = len(books)
    print(f"번역 미생성 도서: {total}권")

    failed = 0
    for i, book in enumerate(books, 1):
        to_korean = book.language != "KR"
        try:
            t_title, t_author = translate(book.title, book.author or "", to_korean)
            book.translated_title = t_title
            book.translated_author = t_author
            book.save(update_fields=["translated_title", "translated_author"])
            if i % 100 == 0 or i == total:
                direction = "→KR" if to_korean else "→DE"
                print(f"  [{i}/{total}] {direction} {book.title[:40]}")
        except Exception as exc:
            failed += 1
            print(f"  [{i}/{total}] 실패 — {book.title[:40]}: {exc}")

    print(f"\n완료: {total - failed}권 생성, {failed}권 실패")


if __name__ == "__main__":
    main()
