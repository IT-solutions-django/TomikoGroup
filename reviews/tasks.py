import os
from celery import shared_task 
from dotenv import load_dotenv
from .models import Review, ReviewPlatform
from .services import (
    get_2gis_reviews_data, 
    get_vl_reviews_data,
)
from .exceptions import UpdateReviewError, EmptyReviewList
from django.db import connection


@shared_task(bind=True, max_retries=5)
def update_2gis_reviews_task(self) -> None: 
    gis_api_key = os.getenv('2GIS_API_KEY')
    organization_id = os.getenv('2GIS_ORGANIZATION_ID')

    try:
        info = get_2gis_reviews_data(
            api_key_2gis=gis_api_key, 
            organization_id=organization_id,
            reviews_limit=10
        )
    except UpdateReviewError as e: 
        raise self.retry(exc=e, countdown=10)
    except EmptyReviewList as e: 
        raise self.retry(exc=e, countdown=10)
    
    reviews = Review.objects.all() 
    new_info = info['reviews']

    if not reviews: 
        for review_info in new_info:
            two_gis, _ = ReviewPlatform.objects.get_or_create(name='2GIS')
            Review.objects.create(
                rate=review_info['stars'], 
                content=review_info['text'], 
                created_at=review_info['created_at'],
                platform=two_gis,
            )

        return

    for i, review in enumerate(reviews):
        review.rate = new_info[i]['stars']
        review.content = new_info[i]['text']
        review.created_at = new_info[i]['created_at']
        review.platform = two_gis
        review.save()


@shared_task(bind=True, max_retries=5)
def update_vl_reviews_task(self): 
    reviews = get_vl_reviews_data() 

    return reviews