from django.contrib import admin
from .models import Editor, Article, Tag

# Register your models here.
"""
We create the ArticleAdmin subclasss that inherits from the ModelAdmin class.
We specify the filter_horizontal property that allows ordering of many to
many fields and pass in the Tag article field

We then pass in the ArticleAdmin subclass as the second argument to our
Article's admin.site.register function.

We reload to see our new updated field.

the 'tags' in ther filter horizontal represents the tag that we have in
the articles model
"""


class ArticleAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags', )


admin.site.register(Editor)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag)
