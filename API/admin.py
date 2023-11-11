from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "organization_name",
                     "amount", "created_at", )
    list_display_links = ("id", "full_name", "created_at")
    search_fields = ("full_name", "organization_name", "created_at", )
    list_filter = ("amount", "created_at")


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "degree", "university", )
    list_display_links = ("id", "full_name")
    search_fields = ("full_name", )
    list_filter = ("degree", "university", )

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", )
    list_display_links = ("id", "name")
    search_fields = ("name", )
    



admin.site.register(StudentSponsor)