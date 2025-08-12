from django.urls import path
from . import views

app_name = 'scraper'

urlpatterns = [
    path('', views.index, name='index'),
    path('scrape/', views.scrape_url, name='scrape_url'),
    path('delete/<int:pk>/', views.delete_scraped_data, name='delete_scraped_data'),
]
