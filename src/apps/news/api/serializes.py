from rest_framework import serializers

from apps.news.models import New
from apps.account.models import User


class NewSerializer(serializers.ModelSerializer):
    """
    Serializer for the New model.
    """

    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = New
        fields = "__all__"
        read_only_fields = ["author"]

    def validate(self, attrs):
        user = self.context["request"].user

        # Check if user can create/edit news
        if user.user_type == User.READER:
            raise serializers.ValidationError(
                "Você não tem permissão para criar/editar notícias"
            )

        # For updates, check if user is the author
        if self.instance and self.instance.author != user:
            raise serializers.ValidationError(
                "Você não tem permissão para editar essa notícia"
            )

        return super().validate(attrs)

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["author"] = user
        return super().create(validated_data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Ensure author is returned as string (ID) for consistency
        if instance.author:
            ret["author"] = str(instance.author.id)
        return ret
