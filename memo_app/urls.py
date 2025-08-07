from django.urls import path
from . import views

urlpatterns = [
    # メモ関連
    path('', views.MemoListView.as_view(), name='memo_list'),
    path('memo/<int:pk>/', views.MemoDetailView.as_view(), name='memo_detail'),
    path('memo/new/', views.MemoCreateView.as_view(), name='memo_create'),
    path('memo/<int:pk>/edit/', views.MemoUpdateView.as_view(), name='memo_update'),
    path('memo/<int:pk>/delete/', views.MemoDeleteView.as_view(), name='memo_delete'),
    
    # お気に入り機能
    path('toggle-favorite/<int:pk>/', views.ToggleFavoriteView.as_view(), name='toggle_favorite'),
    
    # タグ関連
    path('tags/', views.TagListView.as_view(), name='tag_list'),
    path('tags/new/', views.TagCreateView.as_view(), name='tag_create'),
    path('tags/<int:pk>/edit/', views.TagUpdateView.as_view(), name='tag_update'),
    path('tags/<int:pk>/delete/', views.TagDeleteView.as_view(), name='tag_delete'),
    
    # Ajax タグ作成
    path('ajax/tags/create/', views.AjaxTagCreateView.as_view(), name='ajax_tag_create'),
]