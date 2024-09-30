from django.contrib import admin
from .models import ItemCategory, FoodItem

@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'is_active', 'is_deleted', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('is_active', 'is_deleted', 'created_at')

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'is_active', 'is_deleted', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('is_active', 'is_deleted', 'created_at')

