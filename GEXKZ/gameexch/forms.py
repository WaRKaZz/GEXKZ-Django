from django import forms
from .models import GameComment

class GameCommentForm(forms.ModelForm):
	class Meta:
		model = GameComment
		fields = ['message',]
