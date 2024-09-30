from django.contrib import admin
from .models import (
    VendorShopType,
    VendorProfile,
    VendorImages,
    VendorFoodItem,
    VendorFoodItemImage,
    VendorLikes,
    VendorDislikes,
    VendorReview,
    VendorReviewLikes,
    VendrReviewDislikes
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
    list_display = ('vendor', 'image')
    search_fields = ('vendor__vendor_name',)

@admin.register(VendorFoodItem)
class VendorFoodItemAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'food_item')
    search_fields = ('vendor__vendor_name', 'food_item__name')

@admin.register(VendorFoodItemImage)
class VendorFoodItemImageAdmin(admin.ModelAdmin):
    list_display = ('vendor_food_item', 'image')
    search_fields = ('vendor_food_item__vendor__vendor_name',)

@admin.register(VendorLikes)
class VendorLikesAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'user')
    search_fields = ('vendor__vendor_name', 'user__username')

@admin.register(VendorDislikes)
class VendorDislikesAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'user')
    search_fields = ('vendor__vendor_name', 'user__username')

@admin.register(VendorReview)
class VendorReviewAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'item', 'user', 'rating', 'comment')
    search_fields = ('vendor__vendor_name', 'item__food_item__name', 'user__username')
    list_filter = ('rating',)

@admin.register(VendorReviewLikes)
class VendorReviewLikesAdmin(admin.ModelAdmin):
    list_display = ('review', 'user')
    search_fields = ('review__vendor__vendor_name', 'user__username')

@admin.register(VendrReviewDislikes)
class VendrReviewDislikesAdmin(admin.ModelAdmin):
    list_display = ('review', 'user')
    search_fields = ('review__vendor__vendor_name', 'user__username')

