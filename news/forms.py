


from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import LinkSubmission
# from .models import Reply

from .models import Comment_Form, Comment_Reply

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize form fields if needed
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password', 'autocomplete': 'off'})


# class CommentForm(forms.Form):
#     name = forms.CharField(label='Name', max_length=100)
#     email = forms.EmailField(label='Email')
#     comment = forms.CharField(widget=forms.Textarea, label='Comment')

    
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LinkForm(forms.ModelForm):
    class Meta:
        model = LinkSubmission
        fields = ['title', 'url', 'description']

        widgets = {
            'description': forms.Textarea(attrs={'id': 'id_description'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment_Form
        fields = ['comment']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment_Reply
        fields = ['reply']


# class ReplyForm(forms.ModelForm):
#     class Meta:
#         model = Reply
#         fields = ['text']
#         widgets = {
#             'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Reply to this comment...'}),
#         }