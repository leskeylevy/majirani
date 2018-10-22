from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm,ProfileForm,BusinessForm, PostForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .models import Post, Neighbourhood, Business


# Create your views here.
def index(request):
    form = PostForm()
    mabiz = Business.object.filter(neighbourhood=request.user.profile.neighbourhood))
    messages = Post.object.filter(neighbourhood=request.user.profile.neighbourhood)
    if request.method =='POST':
        form=PostForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.neighbourhood = request.user.profile.neighbourhood
            message.save()
            return request('/')
    return render(request, 'index.html', locals())


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)

        return HttpResponse(
            'Thank you for your email confirmation. Now you can' '<a href="/accounts/login"> login </a>your account.')

    else:
        return HttpResponse('Activation link is invalid!')


def profile(request):
    current_user = request.user
    prof = ProfileForm()
    biz = BusinessForm()
    if request.method == 'POST':
        prof = ProfileForm(request.POST,request.FILES,instance=request.user.profile)
        biz = BusinessForm(request.POST)
        if prof.is_valid():
            prf = prof.save(commit=False)
            prf.user = current_user
            prf.save()
            return redirect('profile')
        if biz.is_valid():
            bizna = biz.save(commit=False)
            bizna.user = current_user
            bizna.save()
            return redirect('profile')
    return render(request, 'profile.html', locals())


# def business(request):
#     current_user = request.user
#     biz = BusinessForm()
#     if request.method == 'POST':
#         biz=BusinessForm(request.POST)
#         if biz.is_valid():
#             bizna = biz.save(commit=False)
#             bizna.user = current_user
#             bizna.save()
#     return render(request)