from datetime import datetime
from typing import Any
import requests
from urllib.parse import urlparse
from urllib.parse import parse_qs

from django.conf import settings
from django.db import transaction

from .models import Clip, VkClipInfo


@transaction.atomic
def update_vk_clips() -> None:

    clips_urls = VkClipInfo.objects.all()

    clips_ids = [
        parse_qs(urlparse(clip_url.clip_url).query)["z"][0][4:]
        for clip_url in clips_urls
    ]

    videos_full_info = requests.get(
        f"https://api.vk.ru/method/video.get?videos={','.join(clips_ids)}&access_token={settings.VK_ACCESS_TOKEN}&v=5.199"
    ).json()

    new_clips_data = [
        {
            "id": video_info["id"],
            "title": video_info["title"],
            "thumbnail_url": video_info["image"][-1]["url"],
            "view_count": video_info["views"],
            "url": f'https://vk.com/clips/tomiko_trade?z=clip{video_info["owner_id"]}_{video_info["id"]}',
            "adding_date": datetime.fromtimestamp(video_info["date"]),
        }
        for video_info in videos_full_info["response"]["items"]
    ]

    _delete_old_data()

    _create_clips(new_clips_data)


def _delete_old_data() -> None:
    """
    Удаление старых данных из таблицы Clip.
    """

    Clip.objects.all().delete()


def _create_clips(new_data: list[dict[str, Any]]) -> None:
    """
    Создание записей в БД о клипах.
    :param new_data: Данные для создания.
    """

    for clip in new_data:
        Clip.objects.create(
            name=clip["title"],
            url=clip["url"],
            vk_id=clip["id"],
            thumbnail_url=clip["thumbnail_url"],
            view_count=clip["view_count"],
            adding_date=clip["adding_date"],
        )