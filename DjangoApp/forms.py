from django import forms
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm,PasswordChangeForm
from .models import Post, Tag


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="", max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'email','class': 'forget-pass-box-email','placeholder':'Email address'})
    )

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="",widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'custom-password-input', 'placeholder': 'Please Input Password'}),
    )
    new_password2 = forms.CharField(
        label="",widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'custom-password-input', 'placeholder': 'Please Input Password Again'}),
    )
    
class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    class Meta:
        model = Post
        fields = ['title', 'content', 'address', 'image', 'tags', 'lat', 'lng']

class CustomSetPasswordChange(PasswordChangeForm):
    old_password = forms.CharField(
        label="",widget=forms.PasswordInput(attrs={'autocomplete': 'password','class':'custom-password-input','placeholder': 'Please Input Old Password'}),
    )
    new_password1 = forms.CharField(
        label="",widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'custom-password-input', 'placeholder': 'Please Input Password'}),
    )
    new_password2 = forms.CharField(
        label="",widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'custom-password-input', 'placeholder': 'Please Input Password Again'}),
    )
    
    
