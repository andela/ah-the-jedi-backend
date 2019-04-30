import cloudinary.uploader
import datetime
from rest_framework.response import Response
from .models import User


def ImageUploader(image):
    """
    Upload image to cloudinary
    :param image: FILE from post request
    :return: uploaded image data if image was uploaded successfully else None
    """

    if not str(image.name).endswith(('.png', '.jpg', '.jpeg')):
        return {"status": 400, "error": ["Ensure that the file is an image"]}

    try:
        image_data = cloudinary.uploader.upload(
            image,
            public_id=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                          .replace("-", "")
                          .replace(":", "")
                          .replace(" ", "")),
            crop='limit',
            width=2000,
            height=2000,
            eager=[
                {'width': 200, 'height': 200,
                 'crop': 'thumb', 'gravity': 'face',
                 'radius': 20, 'effect': 'sepia'},
                {'width': 100, 'height': 150,
                 'crop': 'fit', 'format': 'png'}
            ]
        )
        return image_data

    except Exception as e:
        return {"status": e.status_code,
                "error": e.__dict__}


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


def configure_response(serializer):
    """Function to configure response with a user information"""

    dictionary = None
    data = []
    for comment in serializer.data:
        dictionary = dict(comment)
        dictionary['author'] = user_object(dictionary['user_id'])
        del dictionary['user_id']
        data.append(dictionary)
    return data
