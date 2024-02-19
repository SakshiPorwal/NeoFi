# validation

from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']

    def clean_title(self):
        title = self.cleaned_data['title']
        if not title:
            raise forms.ValidationError('Title cannot be empty.')
        return title

    def clean_content(self):
        content = self.cleaned_data['content']
        if not content:
            raise forms.ValidationError('Content cannot be empty.')
        return content
