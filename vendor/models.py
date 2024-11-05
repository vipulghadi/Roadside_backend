from django.db import models
from food_items.models import BaseModel,FoodItem
from users.models import User

types=(('food_truck', 'Food Truck'),
    ('street_stall', 'Street Stall'),
    ('restaurant', 'Restaurant'),
    ('cafe', 'Café'),
    ('catering_service', 'Catering Service'),
    ('cloud_kitchen', 'Cloud Kitchen'),
    ('bakery', 'Bakery'),
    ('ice_cream_parlor', 'Ice Cream Parlor'),
    ('juice_bar', 'Juice Bar'),
    ('barbecue_stall', 'Barbecue Stall'),
    ('diner', 'Diner'),
    ('vegetarian', 'Vegetarian/Vegan Stall'),
    ('fish_and_chips', 'Fish and Chips Shop'),
    ('ethnic_food', 'Ethnic Food Stall'),
    ('patisserie', 'Patisserie'),
    ('food_court', 'Food Court Vendor'),
    ('pop_up', 'Pop-Up Restaurant'),
    ('snack_bar', 'Snack Bar'),
    ('taco_stand', 'Taco Stand'),
    ('dim_sum', 'Dim Sum Stall'),
    ('chaat_stall', 'Chaat Stall'),
    ('sweets_shop', 'Sweets Shop'),
    ('noodle_bar', 'Noodle Bar'),
    ('fried_chicken', 'Fried Chicken Shop'),
    ('salad_bar', 'Salad Bar'),
    ('tandoori_stall', 'Tandoori Stall'),
    ('biryani_shop', 'Biryani Shop'),
    ('kebab_stand', 'Kebab Stand'),
    ('street_pizza', 'Street Pizza'),
    ('gourmet_sandwich', 'Gourmet Sandwich Shop'),)
    
class VendorShopType(BaseModel):
    name=models.CharField(max_length=255,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name or "-"
    class Meta:
        verbose_name_plural = "Vendor Shop Types"
        db_table = "vendor_shop_types"
        

class VendorProfile(BaseModel):
    VENDOR_LOCATION_CHOICES = [
        ('permanent', 'Permanent'),
        ('movable', 'Movable Thela'),
    ]
    FOOD_TYPE_CHOICES = [
        ('veg', 'Veg'),
        ('nonveg', 'Non-Veg'),
        ('all', 'All'),
    ]
    SITTING_CHOICES = [
        ("not available", 'Not available'),
        ('indoor', 'Indoor'),
        ('outdoor', 'Outdoor'),
        ('both', 'Both'),
    ]
    SIZE_CHOICES = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    ]
     
    vendor_name = models.CharField(max_length=255,null=True, blank=True)
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
    vendor_type = models.ForeignKey(VendorShopType,null=True,blank=True,on_delete=models.SET_NULL)
    rating = models.FloatField(default=0.0)  
    reviews_count = models.IntegerField(default=0)  
    opening_days = models.JSONField(blank=True, null=True)
    social_media_links = models.JSONField(null=True, blank=True)  
    establishment_year = models.IntegerField(null=True, blank=True) 
    website_url = models.URLField(null=True, blank=True) 
    
    food_type = models.CharField(max_length=50, choices=FOOD_TYPE_CHOICES, default='veg')
    location_type = models.CharField(max_length=50, choices=VENDOR_LOCATION_CHOICES, default='permanent')
    sitting_available = models.CharField(max_length=50, choices=SITTING_CHOICES, default='both')
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, default='small')
    
    def __str__(self):
        return self.vendor_name or "-"
    
    class Meta:
        verbose_name_plural = "Vendor Profiles"
        db_table = "vendor_profiles"
        
class VendorImages(BaseModel):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name="images",null=True, blank=True)
    image = models.ImageField(upload_to="vendor_images/", blank=True, null=True)
    
    def __str__(self):
        return f"{self.vendor.vendor_name} - Image {self.id}" or '-'
    
    class Meta:
        verbose_name_plural = "Vendor Images"
        db_table = "vendor_images"
    

class VendorFoodItem(BaseModel):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name="vendor_food_items")
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.vendor.vendor_name} - {self.food_item.name}" or '-'
    
    class Meta:
        verbose_name_plural ="Vendor Food Items"
        db_table = "vendor_food_items"

class VendorFoodItemImage(BaseModel):
    vendor_food_item = models.ForeignKey(VendorFoodItem, on_delete=models.CASCADE, related_name="vendor_food_images",null=True,blank=True,)
    image = models.ImageField(upload_to="vendor_food_item_images/",null=True,blank=True)
    
    def __str__(self):
        return f"{self.vendor_food_item}  - Image {self.id}" or '-'
    
    class Meta:
        verbose_name_plural = "Vendor Food Item Images"
        db_table = "vendor_food_item_images"

class VendorLikes(BaseModel):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name="vendor_likes",null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.vendor.vendor_name} - Like {self.id}" or '-'
    
    class Meta:
        verbose_name_plural = "Vendor Likes"
        db_table = "vendor_likes"

class VendorDislikes(BaseModel):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name="vendor_dislikes",null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    
    def __str__(self):
        return f"{self.vendor.vendor_name} - Dislike {self.id}" or '-'
    
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
        return f"{self.vendor.vendor_name} - {self.item.food_item.name} - Review {self.id}" or '-'
    
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


class VendorRating(BaseModel):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name='ratings',null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True) 
    behavior_rating = models.FloatField(default=0.0) 
    service_rating = models.FloatField(default=0.0)   
    quality_rating = models.FloatField(default=0.0)   
    cleanliness_rating = models.FloatField(default=0.0) 
    value_for_money_rating = models.FloatField(default=0.0)  
    overall_rating = models.FloatField(default=0.0)  
    
    def save(self, *args, **kwargs):
        self.overall_rating = (
            self.behavior_rating + self.service_rating + self.quality_rating +
            self.cleanliness_rating + self.value_for_money_rating
        ) / 5
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.vendor.vendor_name} - Rating {self.id}" or '-'
    
    class Meta:
        verbose_name_plural = "Vendor Ratings"
        db_table = "vendor_ratings"

        

    