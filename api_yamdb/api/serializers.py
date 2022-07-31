from rest_framework import serializers, validators
#from django.db.models import Avg
import datetime as dt

from reviews.models import User, Category, Genre, Title, Review, Comment


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):

    genre = GenreSerializer(many=True, )
    """rating = serializers.IntegerField(
        Title.objects.annotate(rating=Avg('reviews__score'))
    )"""

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if (value > year):
            raise serializers.ValidationError('Проверьте год!')
        return value

    def create(self, validated_data):
        if 'genre' not in self.initial_data:
            title = Title.objects.create(**validated_data)
            return title
        else:
            genres = validated_data.pop('genre')
            title = Title.objects.create(**validated_data)
            for genre in genres:
                genre = Genre.objects.get_or_create(
                    **genre)
            return title


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'role',
                  'bio', 'first_name', 'last_name'
                  )


class NotAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'bio',
                  'first_name', 'last_name'
                  )
        read_only_fields = ('role',)


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" не разрешено.'
            )
        return value


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    title = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Review
        validators = (
            validators.UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title'),
                message=('Можно оставить только один отзыв.')
            ),
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    review = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:

        fields = '__all__'
        model = Comment

