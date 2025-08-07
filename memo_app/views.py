from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import Memo, Tag
from .forms import MemoForm, MemoSearchForm, TagForm

class MemoListView(ListView):
    model = Memo
    template_name = 'memo_app/memo_list.html'
    context_object_name = 'memos'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Memo.objects.all()
        form = MemoSearchForm(self.request.GET)
        
        # お気に入りフィルタを追加
        favorite_filter = self.request.GET.get('favorite')
        if favorite_filter == 'true':
            queryset = queryset.filter(is_favorite=True)
        
        if form.is_valid():
            query = form.cleaned_data.get('query')
            tag = form.cleaned_data.get('tag')
            
            if query:
                queryset = queryset.filter(
                    Q(title__icontains=query) | Q(content__icontains=query)
                )
            
            if tag:
                queryset = queryset.filter(tags=tag)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = MemoSearchForm(self.request.GET)
        context['tags'] = Tag.objects.all()
        context['favorite_filter'] = self.request.GET.get('favorite')  # お気に入りフィルタ状態
        return context

class MemoDetailView(DetailView):
    model = Memo
    template_name = 'memo_app/memo_detail.html'
    context_object_name = 'memo'

class MemoCreateView(CreateView):
    model = Memo
    form_class = MemoForm
    template_name = 'memo_app/memo_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'メモを作成しました。')
        return super().form_valid(form)

class MemoUpdateView(UpdateView):
    model = Memo
    form_class = MemoForm
    template_name = 'memo_app/memo_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'メモを更新しました。')
        return super().form_valid(form)

class MemoDeleteView(DeleteView):
    model = Memo
    template_name = 'memo_app/memo_confirm_delete.html' 
    success_url = reverse_lazy('memo_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'メモを削除しました。')
        return super().delete(request, *args, **kwargs)

# お気に入り機能：Ajax対応のビュー
class ToggleFavoriteView(View):
    def post(self, request, pk):
        memo = get_object_or_404(Memo, pk=pk)
        memo.is_favorite = not memo.is_favorite
        memo.save()
        
        return JsonResponse({
            'is_favorite': memo.is_favorite,
            'message': 'お気に入りに追加しました' if memo.is_favorite else 'お気に入りから削除しました'
        })
    
    def get(self, request, pk):
        return JsonResponse({'error': 'Invalid request method'}, status=405)

# タグ管理ビュー
class TagListView(ListView):
    model = Tag
    template_name = 'memo_app/tag_list.html'
    context_object_name = 'tags'
    ordering = ['name']

class TagCreateView(CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'memo_app/tag_form.html'
    success_url = reverse_lazy('tag_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'タグを作成しました。')
        return super().form_valid(form)

class TagUpdateView(UpdateView):
    model = Tag
    form_class = TagForm
    template_name = 'memo_app/tag_form.html'
    success_url = reverse_lazy('tag_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'タグを更新しました。')
        return super().form_valid(form)

class TagDeleteView(DeleteView):
    model = Tag
    template_name = 'memo_app/tag_confirm_delete.html'
    success_url = reverse_lazy('tag_list')
    context_object_name = 'tag'
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'タグを削除しました。')
        return super().delete(request, *args, **kwargs)

# Ajax でタグを作成するビュー（メモ作成時に使用）
class AjaxTagCreateView(View):
    def post(self, request):
        tag_name = request.POST.get('tag_name', '').strip()
        
        if not tag_name:
            return JsonResponse({'error': 'タグ名が入力されていません。'}, status=400)
        
        if Tag.objects.filter(name=tag_name).exists():
            return JsonResponse({'error': 'このタグは既に存在します。'}, status=400)
        
        try:
            tag = Tag.objects.create(name=tag_name)
            return JsonResponse({
                'id': tag.id,
                'name': tag.name,
                'message': f'タグ「{tag.name}」を作成しました。'
            })
        except Exception as e:
            return JsonResponse({'error': 'タグの作成に失敗しました。'}, status=500)