from rest_framework import serializers
from .models import *
from django.db.models import Avg,Sum


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ["id","first_name","last_name","username","password"]

    def create(self, validated_data):
        """
            Register user

        :param validated_data:
        :return:
        """
        try:
            user = User.objects.create(
                username=validated_data['username'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name']
            )
            user.set_password(validated_data['password'])
            user.save()
            return user

        except Exception as e:
            error = {'message': ",".join(e.args) if len(e.args) > 0 else 'Unknown Error'}
            raise serializers.ValidationError(error)


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(instance="author")
    rate = serializers.SerializerMethodField("rate_func")
    user_rate = serializers.SerializerMethodField("user_rate_func")
    def rate_func(self,obj):
        """
            Calculate rate average
        :param obj:
        :return:
        """
        obj.rates.annotate()
        return obj.rates.annotate(sum_rate=Sum("rate_number")).aggregate(average=Avg("sum_rate"))
    def user_rate_func(self,obj):
        """
        Check if user submit rate then return submited rate

        :param obj:
        :return rate_number or None:
        """
        user = self.context['request'].user
        r = obj.rates.filter(user=user).first()
        if r:
            return r.rate_number
        else:
            return None
    class Meta:
        model = Post
        fields = ["id","author","title","description","rate","user_rate"]
