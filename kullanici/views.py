from django.shortcuts import render, reverse, HttpResponseRedirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from deneme.models import Post
from .forms import RegisterForm, LoginForm, UserProfileUpdateForm, UserPasswordChangeForm, UserPasswordChangeForm2
from .models import UserProfile
from deneme.decorators import is_anonymous_required


# Create your views here.

@is_anonymous_required
def register(request):
    form = RegisterForm(data=request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        username = form.cleaned_data.get('username')
        sex = form.cleaned_data.get('sex')
        user.set_password(password)
        user.save()
        userprofile = UserProfile.objects.create(user=user, sex=sex)
        user.userprofile = userprofile
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, '<b>Kayıt olundu</b>', extra_tags='success')
                return HttpResponseRedirect(user.userprofile.get_user_profile_url())
    return render(request, 'kullanici/register.html', context={'form': form})


@is_anonymous_required
def user_login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        password = form.cleaned_data.get('password')
        username = form.cleaned_data.get('username')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                msg = '<b>Merhaba %s hoşgeldin</b>' % username
                messages.success(request, msg, extra_tags='success')
                return HttpResponseRedirect(reverse('post-list'))
    return render(request, 'kullanici/login.html', context={'form': form})


def user_logout(request):
    username = request.user.username
    logout(request)
    msg = '<b>%s</b> hesabından çıkış yapıldı. ' % username
    messages.success(request, msg, extra_tags='success')
    return HttpResponseRedirect(reverse('user-login'))


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    user_post_list = Post.objects.filter(user=user)
    return render(request, 'kullanici/profile/user-profile-page.html',
                  context={'user': user, 'user_post_list': user_post_list})


def user_settings(request):
    sex = request.user.userprofile.sex
    bio = request.user.userprofile.bio
    profile_photo = request.user.userprofile.profile_photo
    initial = {'sex': sex, 'bio': bio, 'profile_photo': profile_photo}
    form = UserProfileUpdateForm(initial=initial, instance=request.user, data=request.POST or None,
                                 files=request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=True)
            bio = form.cleaned_data.get('bio', None)
            sex = form.cleaned_data.get('sex', None)
            profile_photo = form.cleaned_data.get('profile_photo', None)

            user.userprofile.bio = bio
            user.userprofile.sex = sex
            user.userprofile.profile_photo = profile_photo
            user.userprofile.save()
            messages.success(request, 'Profiliniz başarıyla güncellendi', extra_tags='success')
            return HttpResponseRedirect(reverse('user-profile', kwargs={'username': user.username}))
        else:
            messages.warning(request, 'Lütfen girdiğiniz bilgileri kontrol ediniz', extra_tags='danger')

    return render(request, 'kullanici/profile/user-settings.html', context={'form': form})


def user_about(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'kullanici/profile/user-aboutme.html', context={'user': user})


def user_password_change(request):
    # form = UserPasswordChangeForm(user=request.user, data=request.POST or None)
    form = UserPasswordChangeForm2(user=request.user, data=request.POST or None)  # Django PasswordChangeForm
    if form.is_valid():
        # new_password = form.cleaned_data.get('new_password')
        # request.user.set_password(new_password)
        # request.user.save()
        user = form.save(commit=True)  # Django PasswordChangeForm
        update_session_auth_hash(request, user)  # Django PasswordChangeForm
        update_session_auth_hash(request, request.user)
        messages.success(request, 'Şifreniz başarıyla güncellendi', extra_tags='success')
        return HttpResponseRedirect(reverse('user-profile', kwargs={'username': request.user.username}))
    return render(request, 'kullanici/profile/user-password-change.html', context={'form': form})
