# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from users.models import User


# # Here you have to import the User model from your app!


# # admin.site.register(User)
# @admin.register(User)
# class MyUserAdmin(UserAdmin):
#         model = User
#         list_display = ('username',
#                         'email')
#         list_filter = ('username',
#                         'email')
#         search_fields = ('username', )
#         ordering = ('username', )
#         filter_horizontal = ()
#         fieldsets = UserAdmin.fieldsets + (
#                 (None, {'fields': ('username',)}),
#         )
#         # I've added this 'add_fieldset'
#         add_fieldsets = (
#             (None, {
#                 'classes': ('wide',),
#                 'fields': ('username', 'password1', 'password2'),
#             }),
#     )