from django.contrib import admin
from django.conf import settings
from meetup.models import Venue,Event,Group,Member

# class AccountAdmin(admin.ModelAdmin):
#     list_display = ('key','description','container_id','sync')
#     prepopulated_fields = {'slug': ('description',)}
# admin.site.register(Account, AccountAdmin)

class VenueAdmin (admin.ModelAdmin):
    list_display = ('id','name','address_1','city','state')

class GroupAdmin(admin.ModelAdmin):
    list_display = ('id','name','link','n_members')

class EventAdmin(admin.ModelAdmin):
    list_display = ('id','view_when','name','status','group','short_description')
    list_filter = ('status','group')

if getattr(settings,'MEETUP_ALLOW_ADMIN',False):
    admin.site.register(Venue, VenueAdmin)
    admin.site.register(Group, GroupAdmin)
    admin.site.register(Event, EventAdmin)        
