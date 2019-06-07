#!/usr/bin/env python
"""
A package to enable upload of images to Flickr account.
"""
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

        token = FlickrAccessToken(self.API_TOKEN, self.API_TOKEN_SECRET, "write")

        self._flickr = flickrapi.FlickrAPI(
            self.API_KEY, self.API_SECRET, token=token, store_token=False
        )

    def setup_oauth(self):
        f = flickrapi.FlickrAPI(self.API_KEY, self.API_SECRET)

        f.get_request_token(oauth_callback="oob")
        authorize_url = f.auth_url(perms="write")

        webbrowser.open_new_tab(authorize_url)

        verifier = str(input("Verifier code: "))
        f.get_access_token(verifier)

        print("API_TOKEN: {}".format(f.token_cache.token.token))
        print("API_TOKEN_SECRET: {}".format(f.token_cache.token.token_secret))

    def upload(self):
        for file in os.listdir("uploads/"):
            # Skip hidden files (and .gitignore)
            if file.startswith("."):
                continue

            self._flickr.upload(
                filename="uploads/{}".format(file),
                title="Some Title",
                description="Some Description",
                is_public=0,
            )

    @staticmethod
    def clear():
        for file in os.listdir("uploads/"):
            os.remove("uploads/{}".format(file))


def main():
    fu = FlickrUpload()

    fu.upload()


if __name__ == "__main__":
    main()
