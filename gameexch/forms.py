from django import forms
from .models import Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Field
from crispy_forms.bootstrap import FormActions
from django.core.validators import MaxLengthValidator


class CommentForm(forms.ModelForm):

    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': '2'}),
    )

    class Meta:
        model = Comment
        fields = ['message']
