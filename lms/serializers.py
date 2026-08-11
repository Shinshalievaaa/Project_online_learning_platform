from rest_framework import serializers
from lms.models import Course, Lesson, CourseSubscription
from lms.validators import validate_youtube_url


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(
        validators=[validate_youtube_url], required=False, allow_blank=True
    )
    class Meta:
        model = Lesson
        fields = "__all__"
        read_only_fields = ("owner",)


class CourseSerializer(serializers.ModelSerializer):

    is_subscribed = serializers.SerializerMethodField()

    lessons_count = serializers.SerializerMethodField()

    lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_count(self, obj):
        return Lesson.objects.filter(course=obj.id).count()

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return CourseSubscription.objects.filter(
                user=request.user, course=obj.id
            ).exists()
        return False

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "preview",
            "owner",
            "lessons_count",
            "lessons",
            "is_subscribed"
        ]
        read_only_fields = ("owner",)
