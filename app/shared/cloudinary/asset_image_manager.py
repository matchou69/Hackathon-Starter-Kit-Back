"""
Image management with Cloudinary.
"""
import cloudinary
import cloudinary.api
import cloudinary.uploader

PREFIX = "STARTER/"


class AssetImageManager:
    def __init__(self, cloud_name, api_key, cloud_secret):
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=cloud_secret,
        )

    def _upload_image_base64(self, image_base64, new_image_id):
        ret = cloudinary.uploader.upload(image_base64, public_id=new_image_id, format="webp")
        return ret["url"], ret["public_id"]

    def get_resized_image_url(self, image_id, width, height):
        """
        Get the URL of a resized image.
    
        :param image_id: Cloudinary image identifier.
        :param width: Desired width of the resized image.
        :param height: Desired height of the resized image.
        :returns: URL of the resized image.
        """
        url = cloudinary.utils.cloudinary_url(image_id, width=width, height=height, crop="fill")[0]

        return url

    def upload_image_base64(self, image_base64, name):
        """
        Upload an image to cloudinary in the WEBP format

        :param image_base64: image data encoded in base64
        :param name: new image name
        :returns: first item : image_url ; second item : image_id
        """
        if any(c in name for c in '/'):
            raise f'cloudinary name syntaxe error'
        name = PREFIX + "asset/image/" + name
        return self._upload_image_base64(image_base64, name)

    def remove_image_by_id(self, image_id):
        """
        Remove an image from Cloudinary using its public id

        :param image_id: image's Cloudinary id
        :returns: first item : image_url ; second item : image_id
        """
        cloudinary.api.delete_resources(image_id)
