import os 
from celery import Celery 
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TomikoGroup.settings') 

app = Celery('TomikoGroup') 
app.config_from_object('django.conf:settings', namespace='CELERY') 
app.autodiscover_tasks() 

app.conf.beat_schedule = {
    'update_2gis_reviews': {
        'task': 'reviews.tasks.update_2gis_reviews_task',
        'schedule': 10, 
    },
    'update_vl_reviews': {
        'task': 'reviews.tasks.update_vl_reviews_task',
        'schedule': 10, 
    },
}
