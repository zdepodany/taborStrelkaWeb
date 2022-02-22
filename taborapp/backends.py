from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


UserModel = get_user_model()


class EmailBackend(ModelBackend):
    def get_user(self, user_id):
        user = UserModel.objects.filter(pk=user_id)
        if user:
            return user[0]
        else:
            return None

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = UserModel.objects.filter(email=username)
        if not user:
            user = UserModel.objects.filter(username=username)

        # Both username and e-mail are unique. As long as we don't have
        # a very rogue admin, we should be alright.
        if user:
            user = user[0]
        else:
            return None

        if user.check_password(password):
            return user
        else:
            return None

