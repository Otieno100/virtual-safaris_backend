from rest_framework import serializers
from safaris.models import *
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "is_tourist"]

    
class TouristSignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type":"password2"}, write_only=True)
    class Meta:
        model = User
        fields=['username', 'email', 'password','password2']
        extra_kwargs={
            'password':{'write_only':True}
        }

    # def save(self, **kwargs):
    #     user = User(
    #         username=self.validated_data['username'],
    #         email=self.validated_data['email']
    #     )
    #     password =self.validated_data['password'],
    #     # password2 =self.validated_data['password2']
    #     # if password != password2:
    #     #     raise serializers.ValidationError({"error":"passwords did not match"})
    #     user.set_password(password)
    #     user.is_jobseeker = True
    #     user.save()
    #     Jobseeker.objects.create(user=user)
    #     return user
    def save(self, **kwargs):
        user=User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password !=password2:
            raise serializers.ValidationError({"error":"password do not match"})
        user.set_password(password)
        user.is_tourist=True
        user.save()
        Tourist.objects.create(user=user)
        return user

class TourguideSignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type":"password2"}, write_only=True)
    class Meta:
        model = User
        fields=['username', 'email', 'password','password2']
        extra_kwargs={
            'password':{'write_only':True}
        }

    # def save(self, **kwargs):
    #     user = User(
    #         username=self.validated_data['username'],
    #         email=self.validated_data['email']
    #     )
    #     password =self.validated_data['password'],
    #     # password2 =self.validated_data['password2']
    #     # if password!=password2:
    #     #     raise serializers.ValidationError({"error":"passwords did not match"})
    #     user.set_password(password)
    #     user.is_employer = True
    #     user.save()
    #     Employer.objects.create(user=user)
    #     return user

def save(self, **kwargs):
        user=User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password !=password2:
            raise serializers.ValidationError({"error":"password do not match"})
        user.set_password(password)
        user.is_tourguide=True
        user.save()
        Tourguide.objects.create(user=user)
        return user


class UpdateTourguideProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tourguide
        fields = ['name', 'email', 'contact', 'company_bio', 'address', 'company_pic']