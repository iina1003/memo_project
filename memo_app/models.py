from django.db import models
from django.urls import reverse
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='タグ名')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')
    
    class Meta:
        verbose_name = 'タグ'
        verbose_name_plural = 'タグ'
    
    def __str__(self):
        return self.name

class Memo(models.Model):
    title = models.CharField(max_length=200, verbose_name='タイトル')
    content = models.TextField(verbose_name='内容')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='タグ')
    is_favorite = models.BooleanField(default=False, verbose_name='お気に入り')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新日時')
    
    class Meta:
        verbose_name = 'メモ'
        verbose_name_plural = 'メモ'
        ordering = ['-updated_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('memo_detail', kwargs={'pk': self.pk})
    
    def get_content_preview(self, length=100):
        if len(self.content) <= length:
            return self.content
        return self.content[:length] + '...'