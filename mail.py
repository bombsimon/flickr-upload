#!/usr/bin/env python
"""
A daemon that will poll an email inbox (tested with Gmail) every 60 seconds to
see if there's any unread emails with attachments to download and upload to
Flickr.
"""

import email
import imaplib
import os
import time

from flickr_upload.flickr_upload import FlickrUpload


class FetchEmail:
    """
    FetchEmail will scan an email account, parse unread messages and download
    attachments. The downloaded attachments will be uploaded to Flickr.
    """

    EMAIL_IMAP = os.getenv("EMAIL_IMAP", "imap.gmail.com")
    EMAIL_USER = os.getenv("EMAIL_USER", "")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")

    connection = None
    error = None

    def __init__(self):
        self.connection = imaplib.IMAP4_SSL(self.EMAIL_IMAP)
        self.connection.login(self.EMAIL_USER, self.EMAIL_PASSWORD)

    def close_connection(self):
        """
        Close the connection to the IMAP server.
        """
        self.connection.close()

    @staticmethod
    def save_attachment(msg, download_folder="/tmp"):
        """
        Given a message, save its attachments to the specified
        download folder (default is /tmp)

        return: file path to attachment
        """
        att_path = "No attachment found."
        for part in msg.walk():
            if part.get_content_maintype() == "multipart":
                continue

            if part.get("Content-Disposition") is None:
                continue

            filename = part.get_filename()
            att_path = os.path.join(download_folder, filename)

            if not os.path.isfile(att_path):
                fp = open(att_path, "wb")
                fp.write(part.get_payload(decode=True))
                fp.close()

        return att_path

    def fetch_unread_messages(self):
        """
        Retrieve unread messages
        """
        # Select the inbox for writing.
        self.connection.select(readonly=False)

        emails = []
        result, messages = self.connection.search(None, "UnSeen")
        if result != "OK":
            self.error = "Failed to retrieve emails."

            return emails

        for message in messages[0].split():
            try:
                ret, data = self.connection.fetch(message, "(RFC822)")
            except:
                print("No new emails to read.")

                return emails

            msg = email.message_from_bytes(data[0][1])
            if not isinstance(msg, str):
                emails.append(msg)

            self.connection.store(message, "+FLAGS", "\\Seen")

        return emails


def main(sleep_interval=60):
    f = FlickrUpload()

    print("Signing in...")
    e = FetchEmail()

    while True:
        print("Checking for unread messages")

        messages = e.fetch_unread_messages()

        print("Found {} unread messages".format(len(messages)))

        for msg in messages:
            e.save_attachment(msg, "uploads/")

        print("Uploading files to Flickr")
        f.upload()

        print("Removing uploaded files")
        f.clear()

        print("Waiting for {} seconds".format(sleep_interval))
        time.sleep(sleep_interval)


if __name__ == "__main__":
    main()
