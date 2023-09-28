from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Author, Category
from django.utils import timezone

from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class NewsForm(forms.ModelForm):
    postCategory = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple, label='Категория')
    class Meta:
        model = Post
        fields = ['title', 'text', 'author', ]
        labels = {
            'author': 'Автор',
            'title': 'Заголовок',
            'text': 'Текст',
            'postCategory': 'Категория',
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.dateCreation = timezone.now()
        if commit:
            instance.save()
        return instance

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        if text is not None and len(text) < 20:
            raise forms.ValidationError("Текст не может быть менее 20 символов.")

        title = cleaned_data.get("title")
        if title == text:
            raise forms.ValidationError("Текст не должен быть идентичным заголовку.")

        return cleaned_data


class ArticleForm(forms.ModelForm):
    postCategory = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple, label='Категория')
    class Meta:
        model = Post
        fields = ['title', 'text', 'author', ]
        labels = {
            'author': 'Автор',
            'title': 'Заголовок',
            'text': 'Текст',
            'postCategory': 'Категория',
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.dateCreation = timezone.now()
        if commit:
            instance.save()
        return instance

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        if text is not None and len(text) < 20:
            raise forms.ValidationError("Текст не может быть менее 20 символов.")

        title = cleaned_data.get("title")
        if title == text:
            raise forms.ValidationError("Текст не должен быть идентичным заголовку.")

        return cleaned_data


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        common_users = Group.objects.get(name="authors")
        user.groups.add(common_users)
        return user