from django.contrib import admin
from .models import *

admin.site.register(Profile)

""" adds a teacher_request section to the admin site to allow admins to view and accept/deny teacher role change """
@admin.register(Teacher_request)
class TeacherRequestAdmin(admin.ModelAdmin):
    list_display = ['user']
    actions = ['approve_requests']

    def approve_requests(self, request, queryset):
        for teacher_request in queryset:
            teacher_request.user.profile.is_teacher = True
            teacher_request.user.profile.save()
            teacher_request.delete()

        self.message_user(request, "Selected requests have been approved.")

    approve_requests.short_description = "Approve selected requests"