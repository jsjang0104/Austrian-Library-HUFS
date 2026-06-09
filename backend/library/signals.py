import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Book

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Book)
def index_new_book(sender, instance, created, **kwargs):
    """신규 도서가 DB에 저장되는 시점에 HF API로 임베딩을 계산해 검색 인덱스에 추가한다."""
    if not created:
        return
    from . import search_service
    try:
        search_service.add_book(instance)
    except Exception as exc:
        logger.warning("신규 도서(%s) 인덱싱 실패 (벡터 검색에서 제외됨): %s", instance.book_id, exc)
