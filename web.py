#!/usr/bin/env python

from flask import Flask, render_template, redirect, request, flash, url_for
from flickr_upload.flickr_upload import FlickrUpload

app = Flask(__name__)
app.secret_key = "some_secret"

fu = FlickrUpload()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    uploaded_files = request.files.getlist("files")

    if uploaded_files[0].filename == "":
        flash("At least one file must be selected!", "danger")

        return redirect(url_for("index"))

    for file in uploaded_files:
        file.save("uploads/{}".format(file.filename))

        fu.upload()
        fu.clear()

    flash("Uploaded {} images".format(len(uploaded_files)), "info")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0")
