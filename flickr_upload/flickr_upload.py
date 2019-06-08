#!/usr/bin/env python
"""
A package to enable upload of images to Flickr account.
"""
import imghdr
import os
import sys

import flickrapi
import webbrowser

from flickrapi.auth import FlickrAccessToken


class FlickrUpload:
    """
    FlickrUpload implements wrappers to make it easy for you to upload your
    images!
    """

    API_KEY = os.getenv("API_KEY", "")
    API_SECRET = os.getenv("API_SECRET", "")
    API_TOKEN = os.getenv("API_TOKEN", "")
    API_TOKEN_SECRET = os.getenv("API_TOKEN_SECRET", "")

    def __init__(self):
        if not self.API_TOKEN or not self.API_TOKEN_SECRET:
            self.setup_oauth()
            sys.exit(1)

        token = FlickrAccessToken(
            self.API_TOKEN, self.API_TOKEN_SECRET, "write"
        )

        self._flickr = flickrapi.FlickrAPI(
            self.API_KEY, self.API_SECRET, token=token, store_token=False
        )

    def setup_oauth(self):
        """
        To obtain the API token and token secret the very first time this method
        is called if those variables are missing. The function will print the
        values and exit the program.
        """
        f = flickrapi.FlickrAPI(self.API_KEY, self.API_SECRET)

        f.get_request_token(oauth_callback="oob")
        authorize_url = f.auth_url(perms="write")

        webbrowser.open_new_tab(authorize_url)

        verifier = str(input("Verifier code: "))
        f.get_access_token(verifier)

        print("API_TOKEN: {}".format(f.token_cache.token.token))
        print("API_TOKEN_SECRET: {}".format(f.token_cache.token.token_secret))

    def upload(self, src_directory="uploads", is_public=0):
        """
        Upload all files from the given source directory.
        :param src_directory: The directory to upload images from.
        :param is_public: Set to 1 if the images should be public
        """
        for file in os.listdir(src_directory):
            # Skip hidden files (including .gitkeep)
            if file.startswith("."):
                continue

            filename = os.path.join(src_directory, file)
            image_type = imghdr.what(filename)

            # Skip unknown file types
            if image_type is None:
                continue

            # Skip file types that's not images
            if not any(x in image_type for x in ["gif", "jpeg", "png"]):
                continue

            self._flickr.upload(
                filename=filename,
                title="Auto Upload",
                description="Uploaded via python FlickrUpload",
                is_public=is_public,
            )

    @staticmethod
    def clear(src_directory="uploads"):
        """
        Remote all files from given source directory.
        :param src_directory: The directory to remove images from.
        """
        for file in os.listdir(src_directory):
            os.remove(os.path.join(src_directory, file))


def main():
    fu = FlickrUpload()
    fu.upload()


if __name__ == "__main__":
    main()
