from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Snippet

admin.site.site_header = "Klinika"


class SnippetAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')
    list_filter = ('created',)
    change_list_template = 'admin/snippets/snippets_chnage_list.html'


admin.site.register(Snippet, SnippetAdmin)
admin.site.unregister(Group)
