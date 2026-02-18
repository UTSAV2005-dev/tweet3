
from django.shortcuts import render,redirect
from .models import Profile, Tweet ,Comment, review
from .forms import CommentForm, TweetForm,UserRegistrationForm,ProfileEditForm,ReviewForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import JsonResponse
# Create your views here.

def index(request):
    return render(request, 'index.html')


def tweet_list(request):
    tweets = Tweet.objects.all()
    for tweet in tweets:
        tweet.is_liked = tweet.likes.filter(id=request.user.id).exists()

    
    return render(request, 'tweet_list.html', {'tweets': tweets})

def about(request):
    return render(request, 'about.html')



@login_required
def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('reviews')
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form})


@login_required
def reviews(request):
    reviews = review.objects.all().order_by('-created_at')
    return render(request, 'reviews.html', {'reviews': reviews})




@login_required
def tweet_create(request):
    if request.method =='POST':
        form=TweetForm(request.POST,request.FILES)
        if form.is_valid():
            tweet=form.save(commit=False)
            tweet.user=request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form =TweetForm()
    return render(request, 'tweet_form.html', {'form': form})
    
@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id,user=request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet=form.save(commit=False)
            tweet.user=request.user
            form.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet_edit.html', {'form': form})

@login_required
def tweet_delete(request, tweet_id):
    tweet=get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})


@login_required
def comment_edit(request, comment_id):
    # Fetch only the user's own comment for editing
    comment = get_object_or_404(Comment, pk=comment_id, user=request.user)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment) 
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user  # ensures ownership
            comment.save()
            return redirect('tweet_list')
    else:
        form = CommentForm(instance=comment) 
    return render(request, 'comment_edit.html', {'form': form})

@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, user=request.user)
    if request.method == 'POST':
        comment.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {'comment': comment})




def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()   # This already saves with a hashed password if your form extends UserCreationForm
            login(request, user)
            print("Registration successful.")
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})





@login_required
def like_count(request, pk):
    tweet = get_object_or_404(Tweet, id=pk)

    if tweet.likes.filter(id=request.user.id).exists():
        tweet.likes.remove(request.user)
        liked = False
    else:
        tweet.likes.add(request.user)
        liked = True

    return JsonResponse({
        "liked": liked,
        "likes_count": tweet.likes.count()
    })



@login_required
def add_comment(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    if request.method == 'POST':
        body = request.POST.get('body')
        if body:
            Comment.objects.create(tweet=tweet, user=request.user, body=body)
    return redirect(request.META.get('HTTP_REFERER', 'tweet_list'))



@login_required
def profile(request):
    tweets = Tweet.objects.filter(user=request.user)
    return render(request, "profile.html", {
        "profile_user": request.user,  # important!
        "tweets": tweets
    })

def profile_user(request, username):
    """Other user's profile"""
    user = get_object_or_404(User, username=username)
    tweets = Tweet.objects.filter(user=user).order_by("-created_at")
    return render(request, "profile.html", {"profile_user": user, "tweets": tweets})



def profile_edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=profile)
    return render(request, 'profile_edit.html', {'form': form}) 





@login_required
def follow_toggle(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile = profile_user.profile  # assuming Profile has a ManyToManyField `followers`

    if request.user in profile.followers.all():
        profile.followers.remove(request.user)
        following = False
    else:
        profile.followers.add(request.user)
        following = True

    return JsonResponse({
        "following": following,
        "followers_count": profile.followers.count()
    })
