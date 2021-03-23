from django.shortcuts import render, HttpResponse, Http404, get_object_or_404, HttpResponseRedirect, reverse
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.db.models import Q

from .models import Post
from .forms import IletisimForm, ModelForm, CommentForm, PostSearch
from .decorators import is_post, is_anonymous_required


# Create your views here.

@login_required(login_url='/kullanici/login/')
def post_list(request):
    # if not request.user.is_authenticated:
    # return HttpResponseRedirect(reverse('user-login'))
    gelen_deger = request.GET.get('id', None)
    posts = Post.objects.all()
    form = PostSearch(data=request.GET or None)
    if form.is_valid():
        search = form.cleaned_data.get('search', None)
        if search:
            posts = posts.filter(
                Q(text__icontains=search) | Q(title__icontains=search) | Q(kategori__isim__icontains=search))
    page = request.GET.get('page', 1)
    if gelen_deger:
        posts = posts.filter(id=gelen_deger)
    paginator = Paginator(posts, 8)
    try:
        posts = paginator.page(page)
    except EmptyPage:
        posts = paginator.page((paginator.num_pages))
    except PageNotAnInteger:
        posts = paginator.page(1)
    return render(request, 'deneme/post-list.html', context={'posts': posts, 'form': form})


@login_required(login_url=reverse_lazy('user-login'))
def post_update(request, pk):
    # if not request.user.is_authenticated:
    # return HttpResponseRedirect(reverse('user-login'))
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.user:
        return HttpResponseForbidden()
    form = ModelForm(instance=post, data=request.POST or None, files=request.FILES or None)
    if form.is_valid():
        formsave = form.save()
        return HttpResponseRedirect(reverse('post-detail', kwargs={'pk': formsave.pk}))
    context = {'form': form, 'post': post}
    return render(request, 'deneme/post-update.html', context=context)


@login_required(login_url=reverse_lazy('user-login'))
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.user:
        return HttpResponseForbidden()
    post.delete()
    return HttpResponseRedirect(reverse('post-list'))


@login_required(login_url=reverse_lazy('user-login'))
def post_detail(request, pk):
    # if not request.user.is_authenticated:
    # return HttpResponseRedirect(reverse('user-login'))
    form = CommentForm()
    try:
        post = Post.objects.get(pk=pk)
    except:
        raise Http404
    return render(request, 'deneme/post-detail.html', context={'post': post, 'form': form})


@login_required(login_url=reverse_lazy('user-login'))
def post_create(request):
    # if not request.user.is_authenticated:
    # return HttpResponseRedirect(reverse('user-login'))
    form = ModelForm()
    if request.method == "POST":
        deger = request.POST.__str__()
        print(deger)
        form = ModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form_save = form.save(commit=False)
            form_save.user = request.user
            form_save.save()
            msg = "%s isimli postunuz başarıyla oluşturuldu." % (form_save.title)
            messages.success(request, msg, extra_tags='success')
            return HttpResponseRedirect(form_save.get_absolute_url())
        else:
            print('Not valid')
    return render(request, 'deneme/post-create.html', context={'form': form})


@login_required(login_url=reverse_lazy('user-login'))
@is_post
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(data=request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.post = post
        new_comment.user = request.user
        new_comment.save()
        messages.success(request, 'Yorumunuz eklendi')
        return HttpResponseRedirect(reverse('post-detail', kwargs={'pk': post.pk}))
