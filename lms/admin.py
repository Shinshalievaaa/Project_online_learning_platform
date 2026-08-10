from django.contrib import admin

from lms.models import Course, Lesson, CourseSubscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    # list_display = ('id', 'name', 'price', 'price', 'category')
    # list_filter = ('category',)
    search_fields = ('title',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    # list_display = ('id', 'name', 'price', 'price', 'category')
    # list_filter = ('category',)
    search_fields = ('title',)


@admin.register(CourseSubscription)
class CourseSubscriptionAdmin(admin.ModelAdmin):
    # list_display = ('id', 'name', 'price', 'price', 'category')
    # list_filter = ('category',)
    search_fields = ('course',)
