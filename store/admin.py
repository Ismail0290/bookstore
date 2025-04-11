from django.contrib import admin
from .models import Book, Cart, CartItem, Order, OrderItem

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'price', 'stock']
    list_filter = ['created_at']
    search_fields = ['title', 'author']

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    inlines = [CartItemInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'status']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username']
    inlines = [OrderItemInline]