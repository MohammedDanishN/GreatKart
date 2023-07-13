from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages, auth
from .forms import RegisterationForm
from .models import Account
from django.contrib.auth.decorators import login_required

# verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage, send_mail
from django.conf import settings

# Create your views here.


def register_view(request):
    if request.method == "POST":
        form = RegisterationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = Account.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.save()

            # user activation
            current_site = get_current_site(request)
            mail_subject = "GreatKar - Please verify your email address"
            message = render_to_string('accounts/activation.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            from_mail = settings.EMAIL_HOST_USER
            to_email = [email]
            send_mail(mail_subject, message, from_mail, to_email)
            # send_email = EmailMessage(mail_subject, message, to=[to_email])
            # send_email.send()

            return redirect('/accounts/login/?cmd=verification&email='+email)
    else:

        form = RegisterationForm()
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    context = {}
    return render(request, 'accounts/login.html', context)


@login_required(login_url='login')
def logout_view(request):
    auth.logout(request)
    messages.success(request, "logged out successfully")
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Verification Successfull")
        return redirect('login')
    else:
        messages.error(request, 'Invalid Acitvation link')
    return redirect('register')


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            current_site = get_current_site(request)
            mail_subject = "GreatKar - Password reset conformation"
            message = render_to_string('accounts/reset_password_mail.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            from_mail = settings.EMAIL_HOST_USER
            to_email = [email]
            send_mail(mail_subject, message, from_mail, to_email)
            return redirect('/accounts/forgotpassword/?cmd=verification&email='+email)
            messages.success(
                request, 'Password reset mail have been sent to '+email)
            return redirect('login')
        else:
            messages.error(request, "Account does not exist")
            return redirect("forgotpassword")

    return render(request, 'accounts/forgotpassword.html')


def password_reset_validation(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, "Please reset your password")
        return redirect('reset_password')
    else:
        messages.error(request, 'Password reset link expired')
    return redirect("login")


def reset_password(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if confirm_password != password:
            messages.error(request, "Password does not match")
            return redirect('reset_password')
        else:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successfull")
            return redirect('login')
    else:
        return render(request, 'accounts/password_reset.html')
