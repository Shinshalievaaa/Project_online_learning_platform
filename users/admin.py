from django.contrib import admin

from users.models import User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'is_staff', 'is_active', 'is_superuser', 'avatar')
