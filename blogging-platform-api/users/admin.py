from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


# Here you have to import the User model from your app!


admin.site.register(User)
# @admin.register(User)
# class MyUserAdmin(UserAdmin):
#         model = User
#         list_display = ('phone_number',
#                         'email')
#         list_filter = ('phone_number',
#                         'email')
#         search_fields = ('phone_number', )
#         ordering = ('phone_number', )
#         filter_horizontal = ()
#         fieldsets = UserAdmin.fieldsets + (
#                 (None, {'fields': ('phone_number',)}),
#         )
#         # I've added this 'add_fieldset'
#         add_fieldsets = (
#             (None, {
#                 'classes': ('wide',),
#                 'fields': ('phone_number', 'password1', 'password2'),
#             }),
#     )