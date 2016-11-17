from django import forms

from pagedown.widgets import PagedownWidget

from .models import Post

class PostForm (forms.ModelForm):
	text = forms.CharField(widget=PagedownWidget)
	class Meta:
		model = Post
		fields = ('title', 'text',)

