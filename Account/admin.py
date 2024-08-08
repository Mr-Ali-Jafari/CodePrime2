from django.contrib import admin
from .models import Teacher,Participation
# Register your models here.

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('city',)
    search_fields = ('city',"user__username")


@admin.register(Participation)
class ParticipateAdmin(admin.ModelAdmin):
    search_fields = ('name',"user__username")