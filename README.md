# silentlemon

Google calendar-driven light control demo for Helvar intelligent lighting challenge at Junction 2017 hackathlon.

![Logo](silent-lemon-logo.jpg)


## Installation

Requirements: Python 3.6, Google API Python Client, requests

Clone the repo:

    $ git clone https://github.com/axelpale/silentlemon.git

Create silentlemon/silentlemon/client_secret.json with following content. You can find the details from your Google API settings.

    {
      "installed": {
        "client_id": "123456789.apps.googleusercontent.com",
        "project_id": "foo-bar-1234567",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "12345678ABCDEF",
        "redirect_uris": [ "urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
      }
    }


## Run

    $ python3 silentlemon/main.py


## Licence

MIT

Copyright Tiina Ristilä & Akseli Palén
