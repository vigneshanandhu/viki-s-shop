from django.contrib import admin
from .models import Product, Review, Cart

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
    readonly_fields = ('user', 'created_at')
    fields = ('user', 'rating', 'comment', 'created_at')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'image')
    inlines = [ReviewInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'get_username', 'rating', 'comment', 'created_at')
    list_filter = ('rating', 'created_at', 'user')
    search_fields = ('product__name', 'comment', 'user__username')
    
    def get_username(self, obj):
        return obj.user.username if obj.user else 'Anonymous'
    get_username.short_description = 'User'
    get_username.admin_order_field = 'user__username'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'total_price', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('user__username', 'product__name')
    readonly_fields = ('created_at', 'total_price')
