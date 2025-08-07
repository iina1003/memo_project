from django import forms
from .models import Memo, Tag

class MemoForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='タグ'
    )
    
    class Meta:
        model = Memo
        fields = ['title', 'content', 'is_favorite', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'メモのタイトル'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'メモの内容を入力してください...'
            }),
            'is_favorite': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'title': 'タイトル',
            'content': '内容',
            'is_favorite': 'お気に入りに追加'
        }

class MemoSearchForm(forms.Form):
    query = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'メモを検索...'
        }),
        label='検索'
    )
    
    tag = forms.ModelChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        empty_label='すべてのタグ',
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='タグ'
    )

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'タグ名を入力してください',
                'maxlength': '50'
            })
        }
        labels = {
            'name': 'タグ名'
        }
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            name = name.strip()
            if Tag.objects.filter(name=name).exists():
                raise forms.ValidationError('このタグ名は既に使用されています。')
        return name