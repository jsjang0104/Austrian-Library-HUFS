"""번역 필드(translated_title, translated_author, search_text)를 fixtures에서 로드하는 데이터 마이그레이션."""
import json
import os

from django.db import migrations

FIXTURE_PATH = os.path.join(
    os.path.dirname(__file__), "..", "fixtures", "translated_fields.json"
)
BATCH_SIZE = 200


def load_translated_fields(apps, schema_editor):
    Book = apps.get_model("library", "Book")

    with open(FIXTURE_PATH, encoding="utf-8") as f:
        data = json.load(f)

    id_to_data = {item["book_id"]: item for item in data}
    books = list(Book.objects.filter(book_id__in=id_to_data.keys()))

    for book in books:
        row = id_to_data[book.book_id]
        book.translated_title = row.get("translated_title")
        book.translated_author = row.get("translated_author")
        book.search_text = row.get("search_text")

    Book.objects.bulk_update(
        books,
        ["translated_title", "translated_author", "search_text"],
        batch_size=BATCH_SIZE,
    )


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0011_book_translated_fields"),
    ]

    operations = [
        migrations.RunPython(load_translated_fields, migrations.RunPython.noop),
    ]
