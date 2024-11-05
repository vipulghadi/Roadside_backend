from django.db import models

# Create your models here.
from food_items.models import BaseModel

class VendorNotification(BaseModel):
    vendor = models.ForeignKey('vendors.Vendor', on_delete=models.CASCADE)
    sender= models.ForeignKey('users.User', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_seen = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Vendor Notifications"
        db_table = "vendor_notifications"
    
    def __str__(self):
        return f"{self.vendor.vendor_name} - {self.sender.username}: {self.message}" or '-'
    

class UserNotification(BaseModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    sender= models.ForeignKey('users.User', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_seen = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "User Notifications"
        db_table = "user_notifications"
        
    def __str__(self):
        return f"{self.user.username} - {self.sender.username}: {self.message}" or '-'

class GlobalNotification(BaseModel):
    sender= models.ForeignKey('users.User', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    
    class Meta:
        verbose_name_plural = "Global Notifications"
        db_table = "global_notifications"
    
    def __str__(self):
        return f"{self.sender.username}: {self.message}" or '-'



    
