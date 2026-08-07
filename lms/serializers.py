from rest_framework import serializers
from lms.models import Course, Lesson
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

    lessons_count = serializers.SerializerMethodField()

    lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_count(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = ("owner",)
