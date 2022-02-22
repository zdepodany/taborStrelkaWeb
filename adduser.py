from taborapp.models import TaborUser
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

user = TaborUser.objects.create_user("test")

user.email = "test@example.me"
user.set_password("LOLaPublicPassword123")

permissions = []
photo_type = ContentType.objects.get(app_label="taborapp", model="photomodel")

for codename in "view_photomodel", "add_photomodel", "delete_photomodel":
    perm = Permission.objects.filter(content_type=photo_type, codename=codename)
    permissions.append(perm[0])

user.user_permissions.add(*permissions)

user.save()

