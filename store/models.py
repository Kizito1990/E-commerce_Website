from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from PIL import Image


# Create Customer Profile
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	date_modified = models.DateTimeField(User, auto_now=True)
	phone = models.CharField(max_length=20, blank=True)
	address1 = models.CharField(max_length=200, blank=True)
	address2 = models.CharField(max_length=200, blank=True)
	city = models.CharField(max_length=200, blank=True)
	state = models.CharField(max_length=200, blank=True)
	zipcode = models.CharField(max_length=200, blank=True)
	country = models.CharField(max_length=200, blank=True)
	old_cart = models.CharField(max_length=200, blank=True, null=True)

	def __str__(self):
		return f"{self.user.username}'s Profile"

# Create a user Profile by default when user signs up
#def create_profile(sender, instance, created, **kwargs):
	#if created:
		#user_profile = Profile(user=instance)
		#user_profile.save()

# Automate the profile thing
#post_save.connect(create_profile, sender=User)


# Categories of Products
class Category(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

	#@daverobb2011
	class Meta:
		verbose_name_plural = 'categories'


# Customers
class Customer(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	phone = models.CharField(max_length=10)
	email = models.EmailField(max_length=100)
	password = models.CharField(max_length=100)


	def __str__(self):
		return f'{self.first_name} {self.last_name}'



# All of our Products
class Product(models.Model):
	name = models.CharField(max_length=100)
	price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
	description = models.CharField(max_length=250, default='', blank=True, null=True)
	image = models.ImageField(upload_to='uploads/product/')
	# Add Sale Stuff
	is_sale = models.BooleanField(default=False)
	sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)

	def __str__(self):
		return self.name


# Customer Orders
class Order(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	address = models.CharField(max_length=100, default='', blank=True)
	phone = models.CharField(max_length=20, default='', blank=True)
	date = models.DateField(default=datetime.datetime.today)
	status = models.BooleanField(default=False)

	def __str__(self):
		return self.product

#Admins Contact Model
class Contact(models.Model):
	my_address = models.CharField(max_length = 200)
	phone_number = models.CharField(max_length=15)
	my_email = models.EmailField(default=None, max_length=100)

	def __str__(self):
		return self.my_address
	
class Grades(models.Model):
    name = models.CharField(max_length=100)
    price_per_kg = models.DecimalField(decimal_places=2, max_digits=12)
    image = models.ImageField(upload_to='grades/', null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img_path = self.image.path
            img = Image.open(img_path)
            if img.size != (100, 100):
                img = img.convert('RGB')
                img = img.resize((100, 100), Image.ANTIALIAS)
                img.save(img_path)

    class Meta:
		
        verbose_name_plural = 'Grades'

    def __str__(self):
        return f"{self.price_per_kg}"


class PromoVideo(models.Model):
    title = models.CharField(max_length=255)
    video = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Picture(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"