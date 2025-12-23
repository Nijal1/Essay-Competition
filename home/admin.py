# from django.contrib import admin
# from django.contrib.auth import get_user_model
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.utils.translation import gettext_lazy as _
# from .models import Essay

# User = get_user_model()

# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     list_display = ('username','DOB', 'is_staff', 'is_active', 'is_superuser')
#     list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
#     search_fields = ('username',)
#     ordering = ('username',)
#     filter_horizontal = ('groups', 'user_permissions',)

#     # Fields for editing a user
#     fieldsets = (
#         (None, {'fields': ('username', 'password', 'identydoc', 'DOB')}),
#         (_('Permissions'), {'fields': ('is_acitve', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         (_('Important dates'), {'fields': ('last_login',)}),  # remove non-editable fields
#     )

#     # Fields for creating a new user
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'password1', 'password2', 'identydoc', 'DOB', 'is_active', 'is_staff', 'is_superuser'),
#         }),
#     )


# @admin.register(Essay)
# class EssayAdmin(admin.ModelAdmin):
#     list_display = (
#         'id', 'user', 'title', 'score', 'grammar_errors', 'spelling_errors', 
#         'total_errors', 'is_approved', 'is_rejected', 'created_at'
#     )
#     list_filter = ('is_approved', 'is_rejected', 'created_at')
#     search_fields = ('title', 'user__username')
#     ordering = ('-score',)

#     actions = ['approve_essays', 'reject_essays']

#     def approve_essays(self, request, queryset):
#         queryset.update(is_approved=True, is_rejected=False)
#         self.message_user(request, "Selected essays have been approved.")
#     approve_essays.short_description = "Approve selected essays"

#     def reject_essays(self, request, queryset):
#         queryset.update(is_approved=False, is_rejected=True)
#         self.message_user(request, "Selected essays have been rejected.")
#     reject_essays.short_description = "Reject selected essays"




    