import cloudinary.uploader
import datetime
from rest_framework.response import Response


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
