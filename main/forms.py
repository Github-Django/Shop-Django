from main.models import Comment, Compare
from django.forms import ModelForm


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)


class ReplayForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('comment','replay',)


class CompareForm(ModelForm):
    class Meta:
        model = Compare
        fields = ('product',)
