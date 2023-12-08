import razorpay
from django.conf import settings
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from talekarhub.settings import MEDIA_URL
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


def attendance(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please Login and Try Again")
        return redirect('/login')
    SelectTrainer=Trainer.objects.all()
    context={"SelectTrainer":SelectTrainer}
    if request.method=="POST":
        phonenumber=request.POST.get('PhoneNumber')
        Login=request.POST.get('logintime')
        Logout=request.POST.get('loginout')
        SelectWorkout=request.POST.get('workout')
        TrainedBy=request.POST.get('trainer')
        query=Attendance(phonenumber=phonenumber,Login=Login,Logout=Logout,SelectWorkout=SelectWorkout,TrainedBy=TrainedBy)
        query.save()
        messages.warning(request,"Attendace Applied Success")
        return redirect('/attendance')
    return render(request,"attendance.html",context)

def gallery(request):
    posts=Gallery.objects.all()
    context={"posts":posts}
    return render(request,"gallery.html",context)

def services(request):
    services = Service.objects.all()
    print(request.META["HTTP_HOST"])
    print(request.scheme)
    print(MEDIA_URL)
    site_url = request.scheme + "://" + request.META["HTTP_HOST"] + MEDIA_URL
    print(site_url)
    return render(request,"services.html", context={"services": services, "site_url": site_url})


def post_list(request):
    queryset = Post.objects.all()
    context={"blogs":queryset}
    return render(request, 'blog.html', context)

@login_required(login_url='authapp:handlelogin')
def post_blog(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please log in and try again")
        return redirect('/login')

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.user
        image = request.FILES.get('image')  # Use request.FILES to get the uploaded file

        # Create a new Post object with image
        blog_post = Post(title=title, content=content, author=author, img_link=image)
        blog_post.save()

        messages.success(request, "Thanks for posting the blog")
        return redirect('/blog')
    else:
        # Handle the case where the request method is not POST
        messages.warning(request, "Invalid request method")

    return render(request, "post_blog.html")


@login_required(login_url='authapp:handlelogin')
def shop(request):
    products = Product.objects.all()
    
    site_url = request.scheme + "://" + request.META["HTTP_HOST"] + MEDIA_URL
    return render(request,'shop.html', context={'products': products, "site_url": site_url})


def order(request):
    if request.method != "POST":
        messages.warning(request, "Method not allowed!")
        return redirect('/')

    product_id = request.POST.get('product_id')
    address = request.POST.get("address")

    product = Product.objects.filter(id=product_id).last()
    if product is None:
        messages.warning(request, "Product not found!")
        return redirect('/')

    order_obj = Order(product=product, address=address, user=request.user)
    order_obj.save()
    messages.success(request, "Order placed successfully")
    return redirect('/')


def initiate_payment(request):
    product_id = request.GET.get('product_id')
    # address = request.POST.get("address")

    product = Product.objects.filter(id=product_id).last()
    if product is None:
        messages.warning(request, "Product not found!")
        return redirect('/')

    order_obj = Order(product=product, user=request.user)
    order_obj.save()

    if request.method != "POST":
        # messages.warning(request, "Method not allowed!")
        return render(request, 'payment.html', {'order_obj': order_obj, 'product': product})

    amount = 50000  # Amount in paise (e.g., 50 INR)
    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
    

    payment_data = {
        'amount': product.price,
        'currency': 'INR',
        'receipt': f'order_rcptid_{order_obj.id}',
        'payment_capture': '1'
    }

    # Create a Razorpay Order
    order = client.order.create(data=payment_data)

    return JsonResponse(order)


@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        # Perform any necessary actions, such as updating the order status
        # ...
        order_id = request.POST.get('order_id')
        payment_id = request.POST.get('payment_id')

        order = Order.objects.filter(pk=order_id).last()
        # Perform any necessary actions, such as up
        if order is not None:
            order.status = True
            order.save()
            messages.success(request, "Payment successful!")

        return redirect(reverse('authapp:shop'))


    messages.success(request, "Payment unsuccessful!")
    return redirect(reverse('authapp:shop'))

def fetch_data(request):
     last_five_user_data = User.objects.order_by('-last_login')[:5]
     

    #  user_data_with_trainer = Enrollment.objects.select_related(name='Shubham').all()

    #  print(user_data_with_trainer)
     
     return render(request, "fetch_data.html",context={'last_five_user_data': last_five_user_data})