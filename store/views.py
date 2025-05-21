from django.core.paginator import Paginator
from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm

from payment.forms import ShippingForm
from payment.models import ShippingAddress

from django import forms
from django.db.models import Q
import json
from cart.cart import Cart
from .models import Contact, Grades, PromoVideo, Picture
from .forms import ContactForm
from .models import ContactMessage



def index(request):

	return render(request, 'store/index.html')	

def search(request):
	# Determine if they filled out the form
	if request.method == "POST":
		searched = request.POST['searched']
		# Query The Products DB Model
		searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
		# Test for null
		if not searched:
			messages.success(request, "That Product Does Not Exist...Please try Again.")
			return render(request, "store/search.html", {})
		else:
			return render(request, "store/search.html", {'searched':searched})
	else:
		return render(request, "store/search.html", {})	


def update_info(request):
	if request.user.is_authenticated:
		# Get Current User
		current_user = Profile.objects.get(user__id=request.user.id)
		# Get Current User's Shipping Info
		shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
		
		# Get original User Form
		form = UserInfoForm(request.POST or None, instance=current_user)
		# Get User's Shipping Form
		shipping_form = ShippingForm(request.POST or None, instance=shipping_user)		
		if form.is_valid() or shipping_form.is_valid():
			# Save original form
			form.save()
			# Save shipping form
			shipping_form.save()

			messages.success(request, "Your Info Has Been Updated!!")
			return redirect('index')
		return render(request, "store/update_info.html", {'form':form, 'shipping_form':shipping_form})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('store/index')



def update_password(request):
	if request.user.is_authenticated:
		current_user = request.user
		# Did they fill out the form
		if request.method  == 'POST':
			form = ChangePasswordForm(current_user, request.POST)
			# Is the form valid
			if form.is_valid():
				form.save()
				messages.success(request, "Your Password Has Been Updated...")
				login(request, current_user)
				return redirect('update_user')
			else:
				for error in list(form.errors.values()):
					messages.error(request, error)
					return redirect('update_password')
		else:
			form = ChangePasswordForm(current_user)
			return render(request, "update_password.html", {'form':form})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('index')
def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		user_form = UpdateUserForm(request.POST or None, instance=current_user)

		if user_form.is_valid():
			user_form.save()

			login(request, current_user)
			messages.success(request, "User Has Been Updated!!")
			return redirect('index')
		return render(request, "store/update_user.html", {'user_form':user_form})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('index')


def category_summary(request):
	categories = Category.objects.all()
	return render(request, 'store/category_summary.html', {"categories":categories})	

def category(request, foo):
	# Replace Hyphens with Spaces
	foo = foo.replace('-', ' ')
	# Grab the category from the url
	try:
		# Look Up The Category
		category = Category.objects.get(name=foo)
		products = Product.objects.filter(category=category)
		return render(request, 'store/category.html', {'products':products, 'category':category})
	except:
		messages.success(request, ("That Category Doesn't Exist..."))
		return redirect('product')


def product(request,pk):
	product = Product.objects.get(id=pk)
	return render(request, 'store/product.html', {'product':product})

def shop(request):
    products = Product.objects.all()
    paginator = Paginator(products, 8)  # Correctly indented
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'store/products_partial.html', {'page_obj': page_obj})
    
    return render(request, 'store/shop.html', {'page_obj': page_obj})


#About function starts here
def about(request):
	return render(request, 'store/about.html')	

#Login func starts here
def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)

			# Do some shopping cart stuff
			current_user = Profile.objects.get(user__id=request.user.id)
			# Get their saved cart from database
			saved_cart = current_user.old_cart
			# Convert database string to python dictionary
			if saved_cart:
				# Convert to dictionary using JSON
				converted_cart = json.loads(saved_cart)
				# Add the loaded cart dictionary to our session
				# Get the cart
				cart = Cart(request)
				# Loop thru the cart and add the items from the database
				for key,value in converted_cart.items():
					cart.db_add(product=key, quantity=value)

			messages.success(request, ("You Have Been Logged In!"))
			return redirect('index')
		else:
			messages.success(request, ("There was an error, please try again..."))
			return redirect('login')

	else:
		return render(request, 'store/login.html', {})


def logout_user(request):
	logout(request)
	messages.success(request, ("You have been logged out...Thanks for stopping by..."))
	return redirect('index')



def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# log in user
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("Username Created - Please Fill Out Your User Info Below..."))
			return redirect('update_info')
		else:
			messages.success(request, ("Whoops! There was a problem Registering, please try again..."))
			return redirect('register')
	else:
		return render(request, 'store/register.html', {'form':form})
	
		#About Page
def about(request):
    
    return render(request, 'store/about.html')

#Our services
def services(request):
    return render(request, 'store/services.html')

#Admin can change site address and phone number
def site_contact(request):
	contacts = Contact.objects.all()
	
	return render(request, 'store/nav.html', {'contacts':contacts})

#List the grades of different Cashew Nuts
def grades(request):
    query = request.GET.get('q')
    grades = Grades.objects.filter(name__icontains=query) if query else Grades.objects.all()

    paginator = Paginator(grades, 6)  # Show 6 items per page
    page_number = request.GET.get('page')
    grades = paginator.get_page(page_number)

    return render(request, 'store/grade.html', {
        'grades': grades,
        'query': query,
    })


def video(request):
	videos = PromoVideo.objects.all()
	return render(request, 'store/video.html',  {'videos': videos})	


def picture(request):
    pictures = Picture.objects.all()
    return render(request, 'store/picture.html', {'pictures': pictures})



def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(**form.cleaned_data)  # Save to DB
            messages.success(request, "Your message has been sent successfully.")
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'store/contact.html', {'form': form})

def export(request):
    return render(request, 'store/export.html')



def sales(request):
    return render(request, 'store/sales.html' )

def processing(request):
    
    return render(request, 'store/processing.html')

def picture(request):
    pictures = Picture.objects.all()
    return render(request, 'store/picture.html', {'pictures': pictures})