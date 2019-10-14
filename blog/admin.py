from django.contrib import admin
from .models import Post

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display=['title','date_posted','author']
    list_display_links=['title','date_posted']
    list_filter =['date_posted','author']
    search_fields=['title']
    
   

admin.site.register(Post,PostAdmin)