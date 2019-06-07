# Flickr Upload

Upload images to Flickr from a simple web GUI. Flickr used to have an email
associated with each account where one could sent emails to get images uploaded
to the account. This feature is no longer available so here we are, with yet
another implementation of some super well known API...

## How to run the service

You'll need all your API tokens and secrets for the app to work. When you've
obtained your credentials, set the appropriate environment variables. You can
generate your `API_KEY` and `API_SECRET` from your [Flicr
Account](https://www.flickr.com/services/apps/create/apply/) by creating an app.

When you've set your `API_KEY` AND `API_SECRET` you can run the
`flickr_upload.py` file to obtain your `API_TOKEN` AND `API_TOKEN_SECRET`. The
Flicr library does support caching but I chose not to use it.

* `API_KEY`
* `API_SECRET`
* `API_TOKEN`
* `API_TOKEN_SECRET`
