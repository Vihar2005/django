from django.shortcuts import render,redirect
from .models import User,Product,Wishlist,Cart,Blog,Contact
import requests
import random
import stripe
from django.conf import settings
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
from django.http import JsonResponse
from datetime import datetime
# Create your views here.

stripe.api_key = settings.STRIPE_PRIVATE_KEY
YOUR_DOMAIN = 'http://localhost:8000'

def validate_signup(request):
	email=request.GET.get('email')
	data={
		'is_taken':User.objects.filter(email__iexact=email).exists()
	}
	return JsonResponse(data)

@csrf_exempt
def create_checkout_session(request):
	amount = int(json.load(request)['post_data'])
	final_amount=amount*100
	
	session = stripe.checkout.Session.create(
		payment_method_types=['card'],
		line_items=[{
			'price_data': {
				'currency': 'inr',
				'product_data': {
					'name': 'Checkout Session Data',
					},
				'unit_amount': final_amount,
				},
			'quantity': 1,
			}],
		mode='payment',
		success_url=YOUR_DOMAIN + '/success.html',
		cancel_url=YOUR_DOMAIN + '/cancel.html',)
	return JsonResponse({'id': session.id})

def success(request):
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user,payment_status=False)
	for i in carts:
		i.payment_status=True
		i.save()
		
	carts=Cart.objects.filter(user=user,payment_status=False)
	request.session['cart_count']=len(carts)
	return render(request,'success.html')

def cancel(request):
	return render(request,'cancel.html')

def myorder(request):
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user,payment_status=True)
	return render(request,'myorder.html',{'carts':carts})

def index(request):
	products=Product.objects.all()
	return render(request,'index.html',{'products':products})

def blog(request):
	return render(request,'blog.html')

def category(request):
	products=Product.objects.all()
	return render(request,'category.html',{'products':products})

def checkout(request):
	return render(request,'checkout.html')

def contact(request):
	if request.method=="POST":
		Contact.objects.create(
				name=request.POST['name'],
				email=request.POST['email'],
				mobile=request.POST['mobile'],
				message=request.POST['message']
			)
		msg="Contact Saved Successfully"
		return render(request,'contact.html',{'msg':msg})
	else:
		return render(request,'contact.html')

def elements(request):
	return render(request,'elements.html')

def single_blog(request):
	if request.method=="POST":
		Blog.objects.create(
				comment=request.POST['comment'],
				name=request.POST['name'],
				email=request.POST['email'],
				website=request.POST['website']
			)
		msg="Blog Saved Successfully"
		return render(request,'single-blog.html',{'msg':msg})
	else:
		return render(request,'single-blog.html')

def single_product(request):
	return render(request,'single-product.html')

def tracking(request):
	return render(request,'tracking.html')

def login(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			if user.password==request.POST['password']:
				if user.usertype=="buyer":
					request.session['email']=user.email
					request.session['fname']=user.fname
					wishlists=Wishlist.objects.filter(user=user)
					request.session['wishlist_count']=len(wishlists)
					carts=Cart.objects.filter(user=user,payment_status=False)
					request.session['cart_count']=len(carts)
					return render(request,'index.html')
				else:
					request.session['email']=user.email
					request.session['fname']=user.fname
					return render(request,'seller-index.html')
			else:
				msg="Incorrect Password"
				return render(request,'login.html',{'msg':msg})
		except:
			msg="Email Not Registered"
			return render(request,'login.html',{'msg':msg})
	else:
		return render(request,'login.html')

def signup(request):
	if request.method=="POST":
		try:
			User.objects.get(email=request.POST['email'])
			msg="Email Already Registered"
			return render(request,'signup.html',{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:
				User.objects.create(
						fname=request.POST['fname'],
						lname=request.POST['lname'],
						email=request.POST['email'],
						mobile=request.POST['mobile'],
						address=request.POST['address'],
						gender=request.POST['gender'],
						password=request.POST['password'],
						usertype=request.POST['usertype']
					)
				msg="User Sign Up Successfully"
				return render(request,'signup.html',{'msg':msg})
			else:
				msg="Password & Confirm Password Does Not Matched"
				return render(request,'signup.html',{'msg':msg})
	else:
		return render(request,'signup.html')


def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		del request.session['wishlist_count']
		del request.session['cart_count']
		return render(request,'login.html')
	except:
		return render(request,'login.html')


def change_password(request):
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])
		if user.password==request.POST['old_password']:
			if request.POST['new_password']==request.POST['cnew_password']:
				user.password=request.POST['new_password']
				user.save()
				return redirect('logout')
			else:
				msg="New password & Confirm Password Does Not Matched"
				return render(request,'change-password.html',{'msg':msg})
		else:
			msg="New password & Confirm Password Does Not Matched"
			return render(request,'change-password.html',{'msg':msg})
	else:
		return render(request,'change-password.html')


def forgot_password(request):
	if request.method=="POST":
		try:
			mobile=request.POST['mobile']
			User.objects.get(mobile=mobile)
			url = "https://www.fast2sms.com/dev/bulkV2"
			otp=random.randint(1000,9999)
			querystring = {"authorization":"mIk9Ya7tBzZTeAU5C3VGyLwJuRH8ogc2xrqnsKMdPSib6W0jNlQCyZJVL4px2luo8hKgraUk9b3GWejM","variables_values":str(otp),"route":"otp","numbers":str(mobile)}
			headers = {'cache-control': "no-cache"}
			response = requests.request("GET", url, headers=headers, params=querystring)
			print(response.text)
			return render(request,'otp.html',{'mobile':mobile,'otp':otp})
		except:
			msg="Mobile Number Not Registered"
			return render(request,'forgot_password.html',{'msg':msg})
	else:
		return render(request,'forgot_password.html')


def verify_otp(request):
	mobile=request.POST['mobile']
	otp=request.POST['otp']
	uotp=request.POST['uotp']

	if otp==uotp:
		return render(request,'new-password.html',{'mobile':mobile})
	else:
		msg="Invalid OTP"
		return render(request,'otp.html',{'mobile':mobile,'otp':otp,'msg':msg})


def new_password(request):
	mobile=request.POST['mobile']
	np=request.POST['new_password']
	cnp=request.POST['cnew_password']

	if np==cnp:
		user=User.objects.get(mobile=mobile)
		user.password=np
		user.save()
		msg="Password Updated Successfully"
		return render(request,'login.html',{'msg':msg})
	else:
		msg="Password & Confirm Password Does Not Matched"
		return render(request,'new-password.html',{'mobile':mobile,'msg':msg})


def seller_add_product(request):
	seller=User .objects.get(email=request.session['email'])
	if request.method=="POST":
		Product.objects.create(
				seller=seller,
				product_brand=request.POST['product_brand'],
				product_price=request.POST['product_price'],
				product_size=request.POST['product_size'],
				product_pic=request.FILES['product_pic'],
			)
		msg="Product Added Successfully"
		return render(request,'seller-add-product.html',{'msg':msg})
	else:
		return render(request,'seller-add-product.html')


def seller_view_product(request):
	seller=User.objects.get(email=request.session['email'])
	products=Product.objects.filter(seller=seller)
	return render(request,'seller-view-product.html',{'products':products})


def seller_product_details(request,pk):
	product=Product.objects.get(pk=pk)
	return render(request,'seller-product-details.html',{'product':product})	

def product_details(request,pk):
	wishlist_flag=False
	cart_flag=False
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	try:
		Wishlist.objects.get(user=user,product=product)
		wishlist_flag=True
	except:
		pass
	try:
		Cart.objects.get(user=user,product=product)
		cart_flag=True
	except:
		pass
	return render(request,'product-details.html',{'product':product,'wishlist_flag':wishlist_flag,'cart_flag':cart_flag})



def seller_edit_product(request,pk):
	product=Product.objects.get(pk=pk)
	if request.method=="POST":
		product.product_brand=request.POST['product_brand']
		product.product_price=request.POST['product_price']
		product.product_size=request.POST['product_size']
		try:
			product.product_pic=request.FILES['product_pic']
		except:
			pass
		product.save()
		msg="Product Updated Successfully"
		return render(request,'seller-edit-product.html',{'product':product,'msg':msg})
	else:
		return render(request,'seller-edit-product.html',{'product':product})

def seller_delete_product(request,pk):
	product=Product.objects.get(pk=pk)
	product.delete()
	return redirect('seller-view-product')


def add_to_wishlist(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	Wishlist.objects.create(user=user,product=product)
	return redirect('wishlist')


def wishlist(request):
	user=User.objects.get(email=request.session['email'])
	wishlists=Wishlist.objects.filter(user=user)
	request.session['wishlist_count']=len(wishlists)
	return render(request,'wishlist.html',{'wishlists':wishlists})


def remove_from_wishlist(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	wishlist=Wishlist.objects.get(user=user,product=product)
	wishlist.delete()
	return redirect('wishlist')



def add_to_cart(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	Cart.objects.create(
		user=user,
		product=product,
		product_price=product.product_price,
		product_qty=1,
		total_price=product.product_price

		)
	return redirect('cart')


def cart(request):
	net_price=0
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user,payment_status=False)
	for i in carts:
		net_price=net_price+i.total_price
	request.session['cart_count']=len(carts)
	return render(request,'cart.html',{'carts':carts,'net_price':net_price})


def remove_from_cart(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	cart=Cart.objects.get(user=user,product=product)
	cart.delete()
	return redirect('cart')


def change_qty(request):
	pk=int(request.POST['pk'])
	product_qty=int(request.POST['product_qty'])
	cart=Cart.objects.get(pk=pk)
	cart.total_price=cart.product_price*product_qty
	cart.product_qty=product_qty
	cart.save()
	return redirect('cart')


def profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.mobile=request.POST['mobile']
		user.address=request.POST['address']
		user.gender=request.POST['gender']
		try:
			user.profile_pic=request.FILES['profile_pic']
		except:
			pass
		user.save()
		request.session['profile_pic']=user.profile_pic.url 
		msg="Profile Updated Successfully"
		return render(request,'profile.html',{'user':user,'msg':msg})
	else:	
		return render(request,'profile.html',{'user':user})


def base(request):
    # if there are no errors the code inside try will execute
    try:
    # checking if the method is POST
        if request.method == 'POST':
            API_KEY = 'a2ebed383dc3390f328099f10e4e5c86'
            # getting the city name from the form input   
            city_name = request.POST.get('city')
            # the url for current weather, takes city_name and API_KEY   
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric'
            # converting the request response to json   
            response = requests.get(url).json()
            # getting the current time
            current_time = datetime.now()
            # formatting the time using directives, it will take this format Day, Month Date Year, Current Time 
            formatted_time = current_time.strftime("%A, %B %d %Y, %H:%M:%S %p")
            # bundling the weather information in one dictionary
            city_weather_update = {
                'city': city_name,
                'description': response['weather'][0]['description'],
                'icon': response['weather'][0]['icon'],
                'temperature': 'Temperature: ' + str(response['main']['temp']) + ' °C',
                'country_code': response['sys']['country'],
                'wind': 'Wind: ' + str(response['wind']['speed']) + 'km/h',
                'humidity': 'Humidity: ' + str(response['main']['humidity']) + '%',
                'time': formatted_time
            }
        # if the request method is GET empty the dictionary
        else:
            city_weather_update = {}
        context = {'city_weather_update': city_weather_update}
        return render(request, 'home.html', context)
    # if there is an error the 404 page will be rendered 
    # the except will catch all the errors 
    except:
        return render(request, '404.html')
