from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.db.models import Avg, Sum
from django.contrib import messages
from .form import ReviewForm,LoginForm,RegisterForm,OrderForm
from django.contrib.auth import authenticate, login as auth_login,logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import Product, Review, Cart, Order, OrderItem
from django.contrib.auth.models import User
from .decorators import redirect_authenticated_user
from django.http import JsonResponse
from urllib.parse import quote_plus
from decimal import Decimal
import razorpay
from django.conf import settings
import json
import hmac
import hashlib
from django.views.decorators.csrf import csrf_exempt


# Debug: Print Razorpay keys
print("Razorpay Key ID:", settings.RAZORPAY_KEY_ID)
print("Razorpay Key Secret:", settings.RAZORPAY_KEY_SECRET)


# Create your views here.
def index(request):
    return render(request, 'index.html')

def home(request):
    # Exclude test products from the home page
    products = Product.objects.all()
    username = None
    if request.user.is_authenticated:
        username = request.user.username
   
    return render(request, 'home.html', {'products': products, 'username': username})

def product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to submit a review.')
            return redirect('shoppingapp:login')
            
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted successfully!')
            return redirect('shoppingapp:product_detail', product_id=product.id)
        else:
            # Debug: Print form errors to console
            print("Form errors:", form.errors)
            messages.error(request, f'Please correct the errors in your review: {form.errors}')
    else:
        form = ReviewForm()
    
    return render(request, 'product.html', {'product': product, 'form': form, 'username': username})

def product_reviews(request, product_id):
    # Fetch the product
    product = get_object_or_404(Product, id=product_id)
     # All reviews for this product (with user details)
    reviews_qs = (
        Review.objects
        .filter(product=product)
        .select_related("user")
        .order_by("-created_at")
    )
    # Average rating
    avg_rating = reviews_qs.aggregate(Avg("rating"))["rating__avg"] or 0
    # Total reviews
    total_reviews = reviews_qs.count()
    # Ratings count per star
    ratings_count = {
        star: reviews_qs.filter(rating=star).count()
        for star in range(5, 0, -1)
    }
    # Separate current user's review from others
    user_review = None
    other_reviews = reviews_qs
    if request.user.is_authenticated:
        user_review = reviews_qs.filter(user=request.user).first()
        if user_review:
            other_reviews = reviews_qs.exclude(id=user_review.id)
    # Convert reviews into a dictionary list for easier template usage
    def review_to_dict(review):
        return {
            "username": review.user.username if review.user else "Anonymous",
            "rating": review.rating,
            "comment": review.comment,
            "created_at": review.created_at,
        }

    reviews_list = []
    if user_review:
        reviews_list.append(review_to_dict(user_review))
    reviews_list.extend([review_to_dict(r) for r in other_reviews])

    return render(request, "product_reviews.html", {
        "product": product,
        "reviews": reviews_list,
        "avg_rating": avg_rating,
        "total_reviews": total_reviews,
        "ratings_count": ratings_count,
        "user_review": review_to_dict(user_review) if user_review else None
    })

@redirect_authenticated_user
def register(request):
    if request.method =='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request,"Registration Successfull.You can Login")
            return redirect("/login")
    else:
        form = RegisterForm()
    return render(request,'register.html',{'form':form})

@redirect_authenticated_user
def loginpage(request):
    if request.method =='POST':
        #login form
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                auth_login(request,user)
                print("login sucess")
                return redirect("/home")
             
    else:
        form = LoginForm()
    return render(request,'login.html',{'form':form})
def logout(request):
    auth_logout(request)
    return redirect("/")

@login_required
def cart_view(request):
    """Display the user's cart"""
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
    total_price = sum(item.total_price for item in cart_items)
    
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'username': request.user.username
    })

@login_required
def add_to_cart(request, product_id):
    """Add a product to the cart"""
    product = get_object_or_404(Product, id=product_id)
    
    # Check if product already exists in cart
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        # If product exists, increment quantity
        cart_item.quantity += 1
        cart_item.save()
    
    # Instead of Django messages, use alert message via query parameter
    alert_message = f'{product.name} added to cart!'
    return redirect(f"{reverse('shoppingapp:cart')}?alert={quote_plus(alert_message)}")

@login_required
def remove_from_cart(request, product_id):
    """Remove a product from the cart"""
    cart_item = get_object_or_404(Cart, user=request.user, product_id=product_id)
    cart_item.delete()
    alert_message = 'Product removed from cart!'
    return redirect(f"{reverse('shoppingapp:cart')}?alert={quote_plus(alert_message)}")

@login_required
def update_cart(request, product_id):
    """Update cart item quantity"""
    if request.method == 'POST':
        cart_item = get_object_or_404(Cart, user=request.user, product_id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity <= 0:
            cart_item.delete()
            alert_message = 'Product removed from cart!'
        else:
            cart_item.quantity = quantity
            cart_item.save()
            alert_message = 'Cart updated!'
    
    return redirect(f"{reverse('shoppingapp:cart')}?alert={quote_plus(alert_message)}")

@login_required
def order(request):
    """Handle order placement and display order details"""
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
    
    if not cart_items:
        messages.error(request, 'Your cart is empty. Please add items to your cart before placing an order.')
        return redirect('shoppingapp:cart')
    
    # Calculate order totals
    subtotal = sum(item.total_price for item in cart_items)
    shipping = Decimal('50.00')  # Fixed shipping cost
    total_amount = subtotal + shipping
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Create order
            order = form.save(commit=False)
            order.user = request.user
            order.subtotal = subtotal
            order.shipping = shipping
            order.total_amount = total_amount
            order.save()
            
            # Create order items
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price,
                    total_price=cart_item.total_price
                )
            
            # Clear cart
            cart_items.delete()
            
            messages.success(request, 'Order placed successfully! Your order ID is #{}'.format(order.id))
            return redirect('shoppingapp:order_success', order_id=order.id)
    else:
        form = OrderForm(initial={
            'full_name': f"{request.user.first_name} {request.user.last_name}".strip(),
            'email': request.user.email
        })
    
    return render(request, 'order.html', {
        'form': form,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total_amount': total_amount,
        'username': request.user.username
    })
@login_required
@csrf_exempt
def create_razorpay_order(request):
    # Initialize Razorpay client
    razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Create order in database first
            order = Order.objects.create(
                user=request.user,
                full_name=data['full_name'],
                email=data['email'],
                phone=data['phone'],
                address=data['address'],
                city=data['city'],
                zip_code=data['zip_code'],
                subtotal=Decimal(str(data['amount'])) - Decimal('50.00'),
                shipping=Decimal('50.00'),
                total_amount=Decimal(str(data['amount']))
            )

            # Create Razorpay order
            razorpay_order = razorpay_client.order.create({
                'amount': int(data['amount'] * 100),  # Amount in paise
                'currency': 'INR',
                'payment_capture': '1'  # Auto capture
            })

            # Update order with Razorpay order ID
            order.razorpay_order_id = razorpay_order['id']
            order.save()

            return JsonResponse({
                'success': True,
                'order_id': razorpay_order['id'],
                'amount': int(data['amount'] * 100),    # paise
                'order_db_id': order.id,
                'razorpay_key_id': settings.RAZORPAY_KEY_ID  # ✅ send public key
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


@csrf_exempt
def verify_payment(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        payment_data = json.loads(data)

        # Verify payment signature
        generated_signature = hmac.new(
            key=settings.RAZORPAY_KEY_SECRET.encode(),
            msg=f"{payment_data['razorpay_order_id']}|{payment_data['razorpay_payment_id']}".encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        if generated_signature == payment_data['razorpay_signature']:
            # Payment is verified
            order = Order.objects.get(razorpay_order_id=payment_data['razorpay_order_id'])
            order.razorpay_payment_id = payment_data['razorpay_payment_id']
            order.payment_status = 'paid'
            order.save()

            return JsonResponse({'success': True, 'order_id': order.id})
        else:
            return JsonResponse({'success': False, 'error': 'Payment verification failed'}, status=400)

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_success.html', {'order': order})
