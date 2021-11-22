from django.urls import path
from . import views, apps

app_name = apps.BlogConfig.name  # blog
urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.post_detail, name='post_detail'),
    path('tag/<slug:tag_slug>/', views.PostListView.as_view(), name='post_list_by_tag'),
    # path('<int:post_id>/share/', views.post_share, name='post_share'),
]