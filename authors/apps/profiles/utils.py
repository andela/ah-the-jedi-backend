import datetime
import cloudinary.uploader
from django.http import JsonResponse
from rest_framework.exceptions import ParseError

from ..authentication.messages import errors


def ImageUploader(image):
    """
    Upload image to cloudinary
    :param image: FILE from post request
    :return: uploaded image data if image was uploaded successfully else None
    """

    if not str(image.name).endswith(('.png', '.jpg', '.jpeg')):
        raise ParseError(errors["bad_image"])

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
        raise ParseError({"error": e.__dict__})


def validate_image_upload(request):
    """
    Check if image is provided and uploaded

    :param request: put request
    :return: uploaded image data if successful else error raised
    """

    if request.FILES.get("image", False):

        image = ImageUploader(request.FILES["image"])

        request.data["image"] = image.get(
            "secure_url", request.FILES["image"])
