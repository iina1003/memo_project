from django.contrib import admin
from .models import Memo, Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['name']
    
@admin.register(Memo)
class MemoAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at', 'get_tags']
    list_filter = ['created_at', 'updated_at', 'tags']
    search_fields = ['title', 'content']
    filter_horizontal = ['tags']
    ordering = ['-updated_at']
    
    def get_tags(self, obj):
        return ', '.join([tag.name for tag in obj.tags.all()])
    get_tags.short_description = 'タグ'