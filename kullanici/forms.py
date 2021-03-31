from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
import re
from .models import UserProfile


class RegisterForm(forms.ModelForm):
    password = forms.CharField(min_length=6, required=True, label='Şifre',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(min_length=6, required=True, label='Şifre Tekrar',
                                       widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(required=True, label='Cinsiyet', choices=UserProfile.SEX)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'sex', 'username', 'email', 'password', 'password_confirm']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    def clean(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            self.add_error('password', 'Şifreler eşleşmiyor')
            self.add_error('password_confirm', 'Şifreler eşleşmiyor')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email = email.lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Bu email sistemde kayıtlı')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Bu kullanıcı adı sistemde mevcut')
        return username


class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=50, label='Kullanıcı Adı',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(required=True, max_length=50, label='Şifre',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError('Kullanıcı adı veya Şifre hatalı')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if re.match(r"[^@]+@[^@]+\.[^@]+", username):
            users = User.objects.filter(email__iexact=username)
            if len(users) > 0 and len(users) == 1:
                return users.first().username
        return username


class UserProfileUpdateForm(forms.ModelForm):
    sex = forms.ChoiceField(label='Cinsiyet', required=True, choices=UserProfile.SEX)
    profile_photo = forms.ImageField(label='Profil Fotoğrafı', required=False)
    bio = forms.CharField(label='Biyografi', widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ['profile_photo', 'first_name', 'last_name', 'username', 'email', 'sex', 'bio']

    def __init__(self, *args, **kwargs):
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
        self.fields['bio'].widget.attrs['rows'] = 10

    def clean_email(self):
        email = self.cleaned_data.get('email', None)
        # Hiç email bilgisi girilmemişse
        if not email:
            raise forms.ValidationError('Lütfen email bilgisi giriniz')
        # Sistemde olan bir email girilmişse
        if User.objects.filter(email=email).exclude(username=self.instance.username).exists():
            raise forms.ValidationError('Bu email adresi sistemde mevcut.')
        return email


class UserPasswordChangeForm(forms.Form):
    user = None
    old_password = forms.CharField(min_length=6, required=True, label='Mevcut Şifreniz',
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password = forms.CharField(min_length=6, required=True, label='Yeni Şifreniz',
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password_confirm = forms.CharField(min_length=6, required=True, label='Yeni Şifre Doğrulama',
                                           widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserPasswordChangeForm, self).__init__(*args, **kwargs)

    def clean(self):
        new_password = self.cleaned_data.get('new_password')
        new_password_confirm = self.cleaned_data.get('new_password_confirm')
        if new_password != new_password_confirm:
            self.add_error('new_password', 'Yeni şifreler eşleşmedi')
            self.add_error('new_password_confirm', 'Yeni şifreler eşleşmedi')

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('Lütfen mevcut şifrenizi giriniz')
        return old_password


class UserPasswordChangeForm2(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super(UserPasswordChangeForm2, self).__init__(user, *args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
