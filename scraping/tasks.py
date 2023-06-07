import logging

from celery import shared_task
from get_data.delete_old_vacancy import Command

logger = logging.getLogger(__name__)

@shared_task

@shared_task
def delete_old_task():
    """Удаляем старые данные, которым больше 5-дней. Чистим Result и MailingCommerceOffer"""
    Command.handle()
    logger.info(f'model checked and cleaned')