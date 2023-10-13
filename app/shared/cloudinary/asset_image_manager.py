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

    def _upload_image_base64(self, data, new_id):
        """
        :param data: format 64 base expected
        :param new_id: id for the new image
        :returns: first item : image_url ; second item : image_id
        """
        ret = cloudinary.uploader.upload(data, public_id=new_id, format="webp")
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


    def image_upload(self, data, name):
        if any(c in name for c in '/'):
            raise f'cloudinary name syntaxe error'
        name = PREFIX + "asset/image/" + name
        return self._upload_image_base64(data, name)

    def remove_image_by_id(self, id):
        cloudinary.api.delete_resources(id)
