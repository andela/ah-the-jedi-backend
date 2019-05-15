
from authors.apps.authentication.models import User


def user_object(uid):
    """
    Function for getting user object
    """
    instance = User.objects.filter(id=uid)[0]
    user = {
        'id': instance.id,
        'email': instance.email,
        'username': instance.username,
    }

    try:
        user.bio = instance.bio
    except:
        pass
    try:
        user.following = instance.following
    except:
        pass
    try:
        user.image = instance.image
    except:
        pass
    return user
