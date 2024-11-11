from django.contrib import admin
from .models import (
    VendorShopType,
    VendorProfile,
    VendorImages,
    VendorFoodItem,
    VendorFoodItemImage,
    VendorReview,
    
)

@admin.register(VendorShopType)
class VendorShopTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(VendorProfile)
class VendorProfileAdmin(admin.ModelAdmin):
    list_display = ('vendor_name', 'owner', 'address', 'city', 'state', 'zipcode', 'contact_number', 'rating', 'reviews_count')
    search_fields = ('vendor_name', 'owner__username', 'city', 'state')
    list_filter = ('vendor_type', 'establishment_year', 'rating')

@admin.register(VendorImages)
class VendorImagesAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'image_link')
    search_fields = ('vendor__vendor_name',)

@admin.register(VendorFoodItem)
class VendorFoodItemAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'food_item')
    search_fields = ('vendor__vendor_name', 'food_item__name')

@admin.register(VendorFoodItemImage)
class VendorFoodItemImageAdmin(admin.ModelAdmin):
    list_display = ('vendor_food_item', 'image')
    search_fields = ('vendor_food_item__vendor__vendor_name',)


@admin.register(VendorReview)
class VendorReviewAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'user', 'comment')
    search_fields = ('vendor__vendor_name',  'user__username')
    

