from django.db import models

class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True
        
class ItemCategory(BaseModel):
    name = models.CharField(max_length=255,null=True, blank=True)
    image=models.ImageField(upload_to="item_category_images/", blank=True, null=True)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Item Categories"
        db_table = "item_categories"
    
class FoodItem(BaseModel):
    name = models.CharField(max_length=255,null=True, blank=True)
    image=models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_deleted= models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Food Items"
        db_table = "food_items"

    
    