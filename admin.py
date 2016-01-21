from django.contrib import admin
from .models import Profile, MarketItem, Item, Comment, Sharing

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "capital")

class SharingAdmin(admin.ModelAdmin):
    list_display = ("user", "capital")


class MarketItemAdmin(admin.ModelAdmin):
    list_display = ("name", "current_value")

class ItemAdmin(admin.ModelAdmin):
    list_display = ("owner", "value", "time", "sharing")

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Sharing, SharingAdmin)
admin.site.register(MarketItem, MarketItemAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Comment)

