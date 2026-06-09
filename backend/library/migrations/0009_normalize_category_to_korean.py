from django.db import migrations

CATEGORY_MAP = {
    "Literatur": "문학",
    "Sprachwissenschaft": "어학",
    "Linguistik": "어학",
    "Geschichte": "역사",
    "Sozialwissenschaften": "사회과학",
    "Sozialwissenschaft": "사회과학",
    "Sozial과학": "사회과학",
    "Sonstiges": "기타",
    "Sonstige": "기타",
}


def normalize_categories(apps, schema_editor):
    Book = apps.get_model("library", "Book")
    for german, korean in CATEGORY_MAP.items():
        Book.objects.filter(category=german).update(category=korean)


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0008_add_notice_image"),
    ]

    operations = [
        migrations.RunPython(normalize_categories, migrations.RunPython.noop),
    ]
