from rest_framework import serializers
from users.models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True)
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'phone', 'city', 'avatar', 'payments')
        # fields = (
        #     "id",
        #     "email",
        #     "phone",
        #     "city",
        #     "avatar",
        #     "payments",
        # )
        # extra_kwargs = {
        #     # Пароль пишется только при создании/обновлении, в ответе API не возвращается
        #     'password': {'write_only': True}
        # }

    def create(self, validated_data):
        """Создает и возвращает пользователя с захэшированным паролем"""
        # user = User.objects.create_user(**validated_data)
        email = validated_data.pop('email')
        password = validated_data.pop('password', None)
        # 2. Передаем email первым позиционным аргументом, а остальные поля распаковываем
        user = User.objects.create_user(email=email, password=password, **validated_data)
        return user

    def update(self, instance, validated_data):
        """Обновляет пользователя и хэширует пароль при его изменении"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
