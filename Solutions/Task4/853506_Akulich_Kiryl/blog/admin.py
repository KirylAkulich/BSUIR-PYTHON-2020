from django.contrib import admin
from .models import Post,Comment,Account,Composer
# Register your models here.

admin.site.register(Account)
admin.site.register(Composer)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=('title','slug','author','publish',
                  )

    list_filter = ('created','publish','author')
    search_fields=('title','body')
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ('author',)
    date_hierarchy='publish'
    ordering=('publish',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=('name','email','post','created','activate')
    list_filter=('activate','created','updated')
    search_fields = ('name','email','body')