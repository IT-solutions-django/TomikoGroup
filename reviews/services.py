from typing import Any
import requests
from requests.adapters import Retry, HTTPAdapter
from bs4 import BeautifulSoup
from .exceptions import (
    EmptyReviewList, 
    UpdateReviewError
)


def get_2gis_reviews_data(api_key_2gis: str, organization_id: str, reviews_limit: int = 10) -> dict[str, Any]:
    """
    Получаем информацию об отзывах определенной организации
    :param api_key_2gis: 2GIS API KEY
    :param reviews_limit: Количество отзывов в ответе (default: 10);
    :param url: Ссылка на организацию 2 gis 
    :return: Словарь с данными об отзывах организации
    """
    fetched_reviews = _fetch_reviews(organization_id, api_key_2gis)
    result = _get_needed_data_format(fetched_reviews, reviews_limit)
    return result


def _fetch_reviews(organization_id: str, api_key_2gis: str) -> dict[str, dict]:
    """
    Использую публичное API 2gis, получаем полную информацию об отзывах организации.
    :param api_key_2gis: 2GIS API KEY
    :param organization_id: ID организации 2gis
    :return: Словарь ответа 2gis API
    """

    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retries))

    try:
        return session.get(
            f"https://public-api.reviews.2gis.com/2.0/branches/{organization_id}/reviews?"
            f"limit=50&is_advertiser=false&fields=meta.branch_rating&sort_by=date_edited&"
            f"key={api_key_2gis}&locale=ru_RU"
        ).json()
    except Exception:
        raise UpdateReviewError("Ошибка при запросе к 2gis API")


def _get_needed_data_format(
    fetched_data: dict[str, dict], reviews_limit: int = 10
) -> dict[str, Any]:
    """
    Фильтрация ненужных данных ответа и преобразование нужных в необходимый формат.
    :param fetched_data: Данные ответа от API 2gis;
    :param reviews_limit: Количество отзывов в ответе (default: 10);
    :return: Словарь с данными об отзывах организации
    """

    MIN_RATING = 4

    if len(fetched_data["reviews"]) == 0:
        raise EmptyReviewList("Список отзывов пуст")
    
    return {
        "reviews": [
            {
                "stars": review["rating"],
                "created_at": review["date_edited"] or review["date_created"],
                "text": review["text"],
            }
            for review in fetched_data["reviews"]
            if review["rating"] >= MIN_RATING
        ][:reviews_limit],
    }



def get_vl_reviews_data():
    url = "https://www.vl.ru/commentsgate/ajax/thread/company/tomiko-trade/embedded"

    params = {
        "theme": "company",
        "appVersion": "2024101514104",
        "_dc": "0.32945840348689304",
        "pastafarian": "0fb682602c07c4ae9bdb8969e7c43add3b898f4e7b14548c8c2287a29032d6b1",
        "location": "https://www.vl.ru/tomiko-trade#comments",
        "moderatorMode": "1"
    }

    headers = {
        "Host": "www.vl.ru",
        "Sec-Ch-Ua-Platform": "\"macOS\"",
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Language": "ru-RU,ru;q=0.9",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Sec-Ch-Ua": "\"Chromium\";v=\"129\", \"Not=A?Brand\";v=\"8\"",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.71 Safari/537.36",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.vl.ru/autocenter",
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=1, i"
    }

    cookies = {
        "PHPSESSID": "rhjcp9pkfg82bvcda7tve2a9m0",
        "city": "4",
        "region": "103",
        "visitor": "ad5f2acbb35cd457a9dc57c692437d9261e1d5606ea33280caabd64f0fa3d0d6",
        "ring": "980791ab6a297547f26234387e1a5012",
        "analytics_user": "980791ab6a297547f26234387e1a5012",
        "spravochnik_windowSessionID": "ad061bf1730033306880",
        "_ym_uid": "1730033307709177970",
        "_ym_d": "1730033307",
        "sprRecentlyWatchedCompanyIds": "460034",
        "_ym_isad": "2",
        "_gid": "GA1.2.1877505797.1730033311",
        "_ga": "GA1.3.1517315620.1730033307",
        "_ga_3XHX5WMXEB": "GS1.2.1730033312.1.0.1730033312.60.0.0",
        "_ga_D3RZ9TRN3Y": "GS1.3.1730033312.1.0.1730033312.60.0.0",
        "_ga_1XW1PCV9KF": "GS1.2.1730033312.1.1.1730034975.8.0.0",
        "_ym_visorc": "w",
        "spravochnik_windowSessionTS": "1730035316115",
        "_ga_3X07YH0D78": "GS1.1.1730035314.2.1.1730035316.0.0.0",
        "_gat": "1",
        "_gat_allProjects": "1",
        "_gat_glCommonTracker": "1",
        "_gat_commentsvlru": "1",
    }

    response = requests.get(url, headers=headers, params=params, cookies=cookies)

    if response.status_code == 200:
        res = response.json()['data']['content']
        soup = BeautifulSoup(res, 'html.parser')
        review_elements = soup.find_all('li', {'data-type': 'review'})
        reviews = []
        for review in review_elements:
            star_rating = review.find('div', class_='star-rating')
            if star_rating:
                star_rating = int(float(star_rating.find('div', class_='active')['data-value']) * 5)

            user_avatar = review.find('div', class_='user-avatar').find('img')
            if user_avatar:
                user_avatar = user_avatar['src']

            user_name_tag = review.find('span', class_='user-name')
            user_name = user_name_tag.text.strip() if user_name_tag else 'N/A'

            review_text_tag = review.find('div', class_='cmt-content').find('p', class_='comment-text')
            if review_text_tag and "Комментарий:" in review_text_tag.text:
                review_text = review_text_tag.text.strip().split("Комментарий:", 1)[1].strip()
            else:
                continue

            if star_rating >= 4:
                reviews.append({
                    'user_name': user_name,
                    'review_text': review_text,
                    'user_avatar': user_avatar,
                    'star_rating': star_rating
                })

            return reviews

    else:
        print(f"Ошибка: {response.status_code}")