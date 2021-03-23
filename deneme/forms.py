from django import forms
from .models import Post, Comment


class IletisimForm(forms.Form):
    isim = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=50, label='İsim',
                           required=False)
    soyisim = forms.CharField(max_length=50, label='Soyisim', required=False)
    email = forms.EmailField(max_length=50, label='Email', required=True)
    icerik = forms.CharField(max_length=1000, label='İçerik')

    def __init__(self, *args, **kwargs):
        super(IletisimForm, self).__init__((IletisimForm, self).__init__(*args, **kwargs))
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
        self.fields['icerik'] = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    def clean_isim(self):
        isim = self.cleaned_data.get('isim')
        return isim

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email


class ModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'text', 'kategori']

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
        self.fields['text'].widget.attrs['rows'] = 10


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['icerik']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
            self.fields['icerik'].widget.attrs['rows'] = 4


class PostSearch(forms.Form):
    search = forms.CharField(required=False, max_length=500, widget=forms.TextInput(
        attrs={'placeholder': 'Gönderilerde arayın', 'class': 'form-control'}))
