from django.db import models
from food_items.models import BaseModel,FoodItem
from users.models import User

class VendorProfile(BaseModel):
    vendor_name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name="shop")
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=255,null=True, blank=True)
    state = models.CharField(max_length=255,null=True, blank=True)
    zipcode = models.CharField(max_length=20,null=True, blank=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    contact_number = models.CharField(max_length=15)
    alternate_contact_number = models.CharField(max_length=15,null=True, blank=True)
    open_at = models.TimeField(null=True, blank=True)
    close_at=models.TimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Vendor Profiles"
        db_table = "vendor_profiles"
        
class VendorImages(BaseModel):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name="images",null=True, blank=True)
    image = models.ImageField(upload_to="vendor_images/", blank=True, null=True)
    
    def __str__(self):
        return f"{self.vendor} - Image {self.id}"
    
    class Meta:
        verbose_name_plural = "Vendor Images"
        db_table = "vendor_images"
    

class VendorFoodItem(BaseModel):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name="vendor_food_items")
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.vendor} - {self.food_item.name}"
    
    class Meta:
        verbose_name_plural = "Vendor Food Items"
        db_table = "vendor_food_items"

class VendorFoodItemImage(BaseModel):
    vendor_food_item = models.ForeignKey(VendorFoodItem, on_delete=models.CASCADE, related_name="vendor_food_images",null=True,blank=True,)
    image = models.ImageField(upload_to="vendor_food_item_images/",null=True,blank=True)
    
    def __str__(self):
        return f"{self.vendor_food_item}  - Image {self.id}"
    
    class Meta:
        verbose_name_plural = "Vendor Food Item Images"
        db_table = "vendor_food_item_images"

class VendorLikes(BaseModel):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name="vendor_likes",null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.vendor.vendor_name} - Like {self.id}"
    
    class Meta:
        verbose_name_plural = "Vendor Likes"
        db_table = "vendor_likes"

class VendorDislikes(BaseModel):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name="vendor_dislikes",null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    
    def __str__(self):
        return f"{self.vendor.vendor_name} - Dislike {self.id}"
    
    class Meta:
        verbose_name_plural = "Vendor Dislikes"
        db_table = "vendor_dislikes"
        

class VendorReview(BaseModel):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name="vendor_reviews",null=True, blank=True)
    item=models.ForeignKey(VendorFoodItem, on_delete=models.CASCADE, related_name="vendor_food_items",null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    rating = models.IntegerField(default=0)
    comment = models.TextField(null=True,blank=True)
    
    def __str__(self):
        return f"{self.vendor.vendor_name} - {self.item.food_item.name} - Review {self.id}"
    
    class Meta:
        verbose_name_plural = "Vendor Reviews"
        db_table = "vendor_reviews"
    
class VendorReviewLikes(BaseModel):
    review = models.ForeignKey(VendorReview, on_delete=models.CASCADE, null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Vendor Reviews Likes"
        db_table = "vendor_review_likes"

class VendrReviewDislikes(BaseModel):
    review = models.ForeignKey(VendorReview, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)
    
    class Meta:
        verbose_name_plural = "Vendor Reviews Dislikes"
        db_table = "vendor_review_dislikes"
        
        
        
    
    
    
        
    