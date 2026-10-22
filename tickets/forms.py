from django import forms
from .models import Ticket, Comment


class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = [
            "title",
            "description",
            "status",
            "priority",
            "category",
            "tags",
            "attachment",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-contrl",
                    "placeholder": "Ticket title",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "row": 5,
                }
            ),
        }

    # what about naming? and how is this method invoked?
    def clean_title(self):
        title = self.cleaned_data["title"]

        if len(title) < 5:
            raise forms.ValidationError("Name is too short")

        return title


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment

        fields = [
            "text",
        ]
