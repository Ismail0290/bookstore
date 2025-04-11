def cart_items_count(request):
    if request.user.is_authenticated:
        try:
            cart = request.user.cart_set.first()
            if cart:
                return {'cart_items_count': cart.items.count()}
        except:
            pass
    return {'cart_items_count': 0}