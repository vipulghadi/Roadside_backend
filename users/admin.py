from django.contrib import admin
from .models import User, UserProfile, ManagementConfig

# Customizing the UserAdmin class to manage User model in the admin
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'role', 'is_active', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'role')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'state', 'zipcode', 'profile_complete', 'created_at')
    search_fields = ('user__username', 'user__email', 'city', 'state')
    list_filter = ('profile_complete',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

class ManagementConfigAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'created_at', 'updated_at')
    search_fields = ('key',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

# Registering models with custom admin classes
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(ManagementConfig, ManagementConfigAdmin)
