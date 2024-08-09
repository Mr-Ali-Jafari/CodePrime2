from django.contrib import admin
from .models import Teacher,Participation
# Register your models here.

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'family', 'city', 'birthday')
    search_fields = ('city', 'user__username', 'name', 'family')
    list_filter = ('city', 'birthday')
    ordering = ('user', 'name')



@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'family', 'gender', 'city', 'participate_type', 'is_active')
    
    search_fields = ('user__username', 'name', 'family', 'city', 'participate_type')
    
    list_filter = ('gender', 'participate_type', 'city', 'is_active')
    
    ordering = ('-is_active', 'user', 'name')