
from multiprocessing import context
from random import choices
import re
from django.shortcuts import redirect, render , HttpResponse
from . forms  import *
from django.contrib.auth import views 
from django.contrib import messages
from django.views import generic
from django.contrib.auth  import authenticate,  login, logout
from django.contrib.auth.decorators import login_required
import requests
from accounts.models import  Profile
from accounts.forms import ProfileUpdateForm ,UserUpdateForm
from django.core.mail import send_mail,BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes 
from accounts.helpers import send_forget_password_mail 
import uuid
import threading
class EmailThread(threading.Thread):
    def __init__(self,emails):
         self.emails = emails
         threading.Thread.__init__(self)
    def run(self):
         self.emails.send(fail_silently=False)


# Create your views here.

def admin_login(request):
    if request.method=="POST":
        try:
          username = request.POST['username']
          password = request.POST['password']
          user = authenticate(username=username, password=password)
          if user.is_staff:
            login(request, user)
            return redirect("/admin_home")
        except Exception as e:
            messages.error(request, "Invalid Credentials")
                 
    return render(request,"instructor/admin_login.html")


def admin_change_password(request):
    user = request.user
    if request.method == "POST":
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        if user.check_password('{}'.format(old_password)) == False:
              messages.success(request, 'please old password was entered incorrectly Please enter it again.')
        else:        
            if  confirm_password == new_password:
               user.set_password( new_password)
               user.save()
               messages.success(request, 'Your password have chanded successfully.')
               return redirect( '/accounts/admin_login')  
              
            else:
                messages.success(request, 'Password did not match.')
    return render(request, "instructor/admin_change_password.html")






def register(request):
    if request.method=="POST":   
        username = request.POST['username']
        email = request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        branch=request.POST['branch']
        Value = {
               'username':username,
                'firstname':first_name,
                'lastname':last_name,
                'email':email,
                'branch':branch
            }
       
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]') 
        atSymbole = email.index('@')
        dot =email.rfind(".")
        error_mess=""
        if User.objects.filter(username=username).exists():
            error_mess ="This User name have been taken Please try other"
        if User.objects.filter(email=email).exists():
            error_mess ="This email id is already exist"
        if len(username) > 15:  
              error_mess = "username should be under 15 charecter" 
        if(regex.search(username) != None):
                 error_mess = "username must be in alphabets"
                  
        if(regex.search(first_name) != None):
            error_mess = "Name must be in alphabets"  
        if password != confirm_password:  
              error_mess = "Passwords do not match."     
        if  dot != -1:  
            if  (dot <= atSymbole + 3): 
                error_mess = " Please check Your typed email, 3 or 4 character  required before dot"    
            if  (dot != len(email)-4 and dot != len(email)-3):
                error_mess = " Please check Your typed email, After dot, 3 or 2 character required"
        else:
            error_mess = "Please check Your typed email, dot is required after  @"
        if not error_mess:
         user = User.objects.create_user(username, email, password)
         Register.objects.create(user=user,branch=branch)
         user.first_name = first_name
         user.last_name = last_name
         user.save()
         return render(request, 'user_login.html')  

        else:
            context={
                'error':error_mess,
                'values':Value
              } 
            return render(request,"users/register.html",context)       
    return render(request,"users/register.html")




def user_login(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/user_home")
        else:
            messages.error(request, "Invalid Credentials")
                 
    return render(request,"user_login.html")

@login_required
def admin_profile(request):
    user = User.objects.get(id=request.user.id)  
    profile = Profile.objects.filter(user=user).get()  
    instance = profile
    return render(request, "instructor/admin_profile.html")


@login_required
def user_profile(request):
    user = User.objects.get(id=request.user.id)
    data = Register.objects.get(user = user)
    return render(request, "users/user_profile.html",{'data':data})


@login_required
def user_editprofile(request):
    # if request.method == 'POST':
    #     u_form = UserUpdateForm(request.POST, instance=request.user)
    #     p_form = ProfileUpdateForm(request.POST,
    #                                request.FILES,
    #                                instance=request.user.profile)
    #     if u_form.is_valid() and p_form.is_valid():
    #         u_form.save()
    #         p_form.save()
    #         messages.success(request, f'Your account has been updated!')
    #         return redirect('/accounts/user_editprofile')
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    data = Register.objects.get(user = user)
    p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
    if request.method=='POST':
        f = request.POST['firstname']
        l = request.POST['lastname']
        e = request.POST['email']
        b = request.POST['branch']
        user.first_name = f
        user.last_name = l
        data.contact = e
        data.branch = b
        user.save()
        data.save()
        
    else:
        
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'p_form': p_form,
        'data':data,
        'user':user,
    }
    return render(request, 'users/user_editprofile.html',context)




@login_required(login_url = 'login')
def admin_editprofile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('/accounts/admin_editprofile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, "instructor/admin_editprofile.html",context)
    
@login_required
def Logout(request):
    logout(request)
    messages.success(request, 'logout successfully.')
    return redirect('/')
#register and login complted===========================
def change_password_after_login(request):
   
    if request.method=='POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        user = User.objects.get(username__exact = request.user.username)
        if user.check_password('{}'.format(old_password)) == False:
              messages.success(request, 'please old password was entered incorrectly Please enter it again.')
        else:        
            if  confirm_password == new_password:
               user.set_password( new_password)
               user.save()
               messages.success(request, 'Your password have chanded successfully.')
               return redirect( '/accounts/user_login')  
              
            else:
                messages.success(request, 'Password did not match.')

    return render(request,'users/change_password_after_login.html')




def Change_Password(request , token):
    context = {}
    try:
        profile_obj = Profile.objects.filter(forget_password_token = token).first()
        context = {'user_id' : profile_obj.user.id}
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')
            
            if user_id is  None:
                messages.success(request, 'No user id found.')
                return redirect(token)
                
            
            if  new_password != confirm_password:
                messages.success(request, 'password did not match.')
                return redirect(token)
                         
            
            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            messages.success(request, 'Your password have reset successfully.')
            return redirect('/accounts/user_login')
           
    except Exception as e:
        print(e)
    return render(request , 'change_password.html',context )



def forget_Password(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            
            if not User.objects.filter(email=email).first():
                messages.success(request, 'User is not exixt.')
                return redirect('forget_password')
            
            user_obj = User.objects.get(email = email)
            token = str(uuid.uuid4())
            profile_obj= Profile.objects.get(user = user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email , token)
            messages.success(request, 'An email have sent for resetting your password.If you don’t receive  email, please make sure , you have registered with correct email id')
            return redirect('forget_password')
          
    except Exception as e:
        print(e)
    return render(request , 'forget_password.html')


