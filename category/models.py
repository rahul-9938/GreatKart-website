from django.db import models
from django.urls import reverse



class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)  #A slug is a simplified string, often used in URLs to identify a particular resource in a readable and SEO-friendly way.
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)  # category image (optional field)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'  #plural name for the model in the admin interface.
    
    def get_url(self):
        return reverse('products_by_category', args=[self.slug])  #reverse function is used to generate URLs based on the view name and arguments. In this case, it generates a URL for the 'product_by_category' view, passing the category's slug as an argument.
    
    def __str__(self):
        return self.category_name