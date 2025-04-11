from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Book, Cart, CartItem, Order, OrderItem

def book_list(request):
    books = Book.objects.all()
    return render(request, 'store/book_list.html', {'books': books})

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'store/book_detail.html', {'book': book})

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    try:
        cart_item = CartItem.objects.get(cart=cart, book=book)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        CartItem.objects.create(cart=cart, book=book)
    
    messages.success(request, f"{book.title} added to your cart.")
    return redirect('store:cart')

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, "Item removed from your cart.")
    return redirect('store:cart')

@login_required
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            item.quantity = quantity
            item.save()
        else:
            item.delete()
    
    return redirect('store:cart')

@login_required
def cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
    except Cart.DoesNotExist:
        cart = None
        cart_items = []
    
    total = sum(item.get_cost() for item in cart_items)
    return render(request, 'store/cart.html', {'cart': cart, 'cart_items': cart_items, 'total': total})

@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
        if not cart_items:
            messages.warning(request, "Your cart is empty.")
            return redirect('store:book_list')
    except Cart.DoesNotExist:
        messages.warning(request, "Your cart is empty.")
        return redirect('store:book_list')
    
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        
        # Validate data
        if not address or not phone:
            messages.error(request, "Please provide both address and phone number.")
            return render(request, 'store/checkout.html', {
                'cart_items': cart_items,
                'total': sum(item.get_cost() for item in cart_items),
                'address': address,
                'phone': phone
            })
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            address=address,
            phone=phone
        )
        
        # Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                price=item.book.price,
                quantity=item.quantity
            )
        
        # Clear the cart
        cart.delete()
        
        return redirect('store:order_complete', order_id=order.id)
    
    # Pre-fill with user profile data if available
    initial_address = ''
    initial_phone = ''
    if hasattr(request.user, 'profile'):
        initial_address = request.user.profile.address or ''
        initial_phone = request.user.profile.phone or ''
    
    total = sum(item.get_cost() for item in cart_items)
    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'address': initial_address,
        'phone': initial_phone
    })

@login_required
def order_complete(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_complete.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})