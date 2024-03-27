from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utils import TokenGenerator,generate_token
from django.utils.encoding import force_bytes,DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.generic import View
from django.utils.encoding import force_str
from django.contrib.auth import authenticate,logout,login
from .forms import UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
# Create your views here.
def register(request):
   if request.method == 'POST':
       firstname=request.POST['firstname']
       lastname=request.POST['lastname']
       email=request.POST['email']
       password=request.POST['password']
       cpassword=request.POST['cpassword']
       if password != cpassword:
           messages.info(request,"Wrong password")
           return redirect('register')

       try:
           if User.objects.get(username=email):
               messages.info(request,'Username already taken')
               return redirect('register')
       except Exception as e:
           pass
       user=User.objects.create_user(username=email,email=email,password=password,first_name=firstname,last_name=lastname)
       user.is_active=False
       user.save()
       current_site = get_current_site(request)
       email_subject = "activate Your Account"
       message = render_to_string('activate.html', {
           'user': user,
           'domain': current_site,
           #'domain': '127.0.0.1:8000',
           'uid': urlsafe_base64_encode(force_bytes(user.pk)),
           'token': generate_token.make_token(user),

       })
       email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email])
       email_message.send()
       messages.info(request, "Activate your Accounts by clicking the link in your gmail")
       # return redirect('signin')
       #return redirect('signin/?command=verification&email='+email)
   return render(request,'register.html')

class ActivateAccountView(View):
    def get(self,request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.info(request,'Your account has been activated successfully')
            return redirect('signin')
        return render(request,'activatefail.html')
def signin(request):
    if request.method == 'POST':
        username=request.POST['email']
        password=request.POST['password']
        myuser=authenticate(username=username,password=password)
        if myuser is not None:
            login(request,myuser)
            # messages.success(request,"Login success")
            return redirect('/')
        else:
            messages.error(request,"Invalid credential")
            return redirect('signin')

    return render(request,'signin.html')

def log_out(request):
    logout(request)
    # messages.info(request,'Log out success')
    return redirect('/')

@login_required
def profile(request):

    return render(request,'profile.html')
def profileUpdate(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            username=request.user.first_name
            messages.success(request,f'{username},Your account has been updated')
            return redirect('profile')
    else:
         u_form = UserUpdateForm(instance=request.user)
         p_form = ProfileUpdateForm(instance=request.user.profile)
    context ={
        'u_form' : u_form,
        'p_form' : p_form,
    }
    return render(request,'profileupdate.html',context)

def forgotPassword(request):
    if request.method == 'POST':
        email=request.POST['email']
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email__exact=email)

            #reset password email
            current_site=get_current_site(request)
            email_subject = "Reset your password"
            message = render_to_string('reset_password.html', {
                'user': user,
                'domain': current_site,
                #encoding user primary key
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                #create token for particular user
                'token': generate_token.make_token(user),

            })
            email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email])
            email_message.send()
            messages.info(request, "Password reset email has been sent to your email adderess.")
            return redirect('signin')
        else:
            messages.error(request,'Account does not exixst')
            return redirect('forgotPassword')

    return render(request,'forgot_password.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as identifier:
        user = None
    if user is not None and generate_token.check_token(user, token):
        request.session['uid']=uid
        messages.success(request,'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request,'This link has been expired')
        return redirect('signin')

def resetPassword(request):
    if request.method == 'POST':
        password= request.POST['password']
        conf_password=request.POST['cpassword']
        if password == conf_password:
            uid=request.session.get('uid')
            user=User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password reset success')
            return redirect('signin')
        else:
            messages.error(request,'Password not match')
            return redirect('resetPassword')
    else:
        return render(request,'resetPassword.html')

@login_required(login_url='signin')
def changePassword(request):
    if request.method=='POST':
        current_password=request.POST['current_password']
        new_password = request.POST['new_password']
        cofirm_password = request.POST['conf_password']
        user=User.objects.get(username__exact=request.user.username)
        if new_password == cofirm_password:
            success=user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                #auth.logout(request)
                messages.success(request,'Password updated successfully')
                return redirect('changePassword')
            else:
                messages.error(request,'Please enter valid current password')
                return redirect('changePassword')
        else:
            messages.error(request,'Password does not match')
            return redirect('changePassword')

    return render(request,'change_password.html')

