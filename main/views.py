import razorpay
from django.conf import settings
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
# from azwafitness.settings import MEDIA_URL
from main.models import Contact, MembershipPlan, Trainer, Enrollment, Gallery, Attendance, Service, Product, Order
from django.contrib.auth.decorators import login_required
from .models import Post
# from .tables import PostTable
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def Home(request):

    return render(request,"index.html")

def signup(request):
    if request.method=="POST":
        username=request.POST.get('usernumber')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
      
        if len(username)>10 or len(username)<10:
            messages.info(request,"Phone Number Must be 10 Digits")
            return redirect('/signup')

        if pass1!=pass2:
            messages.info(request,"Password is not Matching")
            return redirect('/signup')
       
        try:
            if User.objects.get(username=username):
                messages.warning(request,"Phone Number is Taken")
                return redirect('/signup')
           
        except Exception as identifier:
            pass
        
        
        try:
            if User.objects.get(email=email):
                messages.warning(request,"Email is Taken")
                return redirect('/signup')
           
        except Exception as identifier:
            pass
        
        
        
        myuser=User.objects.create_user(username,email,pass1)
        myuser.save()
        messages.success(request,"User is Created Please Login")
        return redirect('/login')
        
        
    return render(request,"signup.html")

def handlelogin(request):
    if request.method=="POST":        
        username=request.POST.get('usernumber')
        pass1=request.POST.get('pass1')
        myuser=authenticate(username=username,password=pass1)
        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Login Successful")
            return redirect('/')
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('/login')
            
        
    return render(request,"handlelogin.html")

def handleLogout(request):
    logout(request)
    messages.success(request,"Logout Success")    
    return redirect('/login')


@login_required(login_url='main:handlelogin') 
def enroll(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please Login and Try Again")
        return redirect('/login')

    memberships = MembershipPlan.objects.all()
    trainers = Trainer.objects.all()

    context = {"memberships": memberships, "trainers": trainers}

    if request.method == "POST":
        full_name = request.POST.get('FullName')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('PhoneNumber')
        dob = request.POST.get('DOB')
        member = request.POST.get('member')
        
        # Get the trainer instance based on the selected trainer ID
        trainer_id = request.POST.get('trainer')
        selected_trainer = Trainer.objects.get(pk=trainer_id)

        reference = request.POST.get('reference')
        address = request.POST.get('address')

        # Use the selected trainer instance in the Enrollment creation
        query = Enrollment(
            FullName=full_name,
            Email=email,
            Gender=gender,
            PhoneNumber=phone_number,
            DOB=dob,
            SelectMembershipplan=member,
            SelectTrainer=selected_trainer,  # Use the selected trainer instance
            Reference=reference,
            Address=address
        )
        query.save()

        messages.success(request, "Thanks For Enrollment")
        return redirect('/')
    
    return render(request, 'enroll.html', context)


def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please Login and Try Again")
        return redirect('/login')
    user_phone=request.user
    posts=Enrollment.objects.filter(PhoneNumber=user_phone)
    attendance=Attendance.objects.filter(phonenumber=user_phone)
    context={"posts":posts,"attendance":attendance}
    return render(request,"profile.html",context)


def contact(request):
    if request.method=="POST":
        name=request.POST.get('fullname')
        email=request.POST.get('email')
        number=request.POST.get('num')
        desc=request.POST.get('desc')
        myquery=Contact(name=name,email=email,phonenumber=number,description=desc)
        myquery.save()       
        messages.info(request,"Thanks for Contacting us we will get back you soon")
        return redirect('/contact')
        
    return render(request,"contact.html")