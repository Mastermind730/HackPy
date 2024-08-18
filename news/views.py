from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import LoginForm, RegisterForm, CommentForm, ReplyForm, LinkForm
from .models import CrawlHackerNews, Vote, Comment_Form, Comment, LinkSubmission
import logging
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.contrib.auth import logout
from django.shortcuts import redirect


logger = logging.getLogger(__name__)

def news_list(request):
    news_items = CrawlHackerNews.objects.all().order_by('-date')
    paginator = Paginator(news_items, 10)  # Show 10 news items per page
    user = request.user
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news_list.html', {'page_obj': page_obj, "user": user})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            form.add_error(None, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def comments_view(request):
    comments = Comment_Form.objects.all()
    comment_form = CommentForm()
    reply_forms = {comment.id: ReplyForm() for comment in comments}

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'comment_form':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.name = request.user.username
                new_comment.email = request.user.email
                new_comment.save()
                return redirect('comments_view')
        elif form_type.startswith('reply_form_'):
            comment_id = int(form_type.split('_')[-1])
            comment = get_object_or_404(Comment_Form, id=comment_id)
            reply_form = ReplyForm(request.POST)
            if reply_form.is_valid():
                new_reply = reply_form.save(commit=False)
                new_reply.comment = comment
                new_reply.user = request.user
                new_reply.save()
                return redirect('comments_view')

    context = {
        'comments': comments,
        'comment_form': comment_form,
        'reply_forms': reply_forms
    }
    return render(request, 'comment_list.html', context)

@login_required
def submit_link(request):
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.user = request.user
            link.save()
            return redirect('link_success')  # Redirect to a relevant view after submission
    else:
        form = LinkForm()
    return render(request, 'submit_link.html', {'form': form})

def link_success_view(request):
    return render(request, 'comment_success.html')

@login_required
def link_submission_list(request):
    links = LinkSubmission.objects.all()
    return render(request, 'link_submission_list.html', {'links': links})

@login_required
def detail(request, news_id):
    news_item = get_object_or_404(CrawlHackerNews, pk=news_id)
    return render(request, 'news/detail.html', {'news_item': news_item, 'news_id': news_id})

def vote(request, news_id):
    if request.method == 'POST':
        user = request.user
        news = CrawlHackerNews.objects.get(id=news_id)
        vote_type = request.POST.get('vote_type')

        vote, created = Vote.objects.get_or_create(user=user, news=news)
        if vote_type == 'upvote':
            vote.vote_type = 'upvote'
        else:
            vote.vote_type = 'downvote'
        vote.save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def search(request):
    query = request.GET.get('q')
    if query:
        news_items = CrawlHackerNews.objects.filter(title__icontains=query)
    else:
        news_items = CrawlHackerNews.objects.none()

    paginator = Paginator(news_items, 10)
    page = request.GET.get('page')
    try:
        news_items = paginator.page(page)
    except PageNotAnInteger:
        news_items = paginator.page(1)
    except EmptyPage:
        news_items = paginator.page(paginator.num_pages)

    return render(request, 'news/search.html', {'news_items': news_items, 'query': query})

def index(request):
    news_items = CrawlHackerNews.objects.all().order_by('-date')
    logger.info(f"Fetched news items: {news_items}")
    return render(request, 'news/index.html', {'news_items': news_items})



def logout_view(request):
    logout(request)
    return redirect('login')
