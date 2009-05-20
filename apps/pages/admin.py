from django.contrib import admin
from pages.models import Page


class PageAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "pub_date", "active")
    list_filter = ("active",)
    list_display_links = ("id", "title")
    prepopulated_fields = {"slug": ("title",)}
    
admin.site.register(Page, PageAdmin)