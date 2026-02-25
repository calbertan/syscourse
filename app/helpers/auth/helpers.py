#!/usr/bin/env python
import requests
import time
import google.auth.crypt
import google.auth.jwt
from google.auth.transport.requests import AuthorizedSession
def generate_creds(sa_keyfile, sa_email, audience):
    """
    Here we generate a signed JSON Web Token using a IAM Service Account.
    :param sa_keyfile:    Service account key file
    :param sa_email:      Service Account
    :param audience:      Token recipient
    """
    # Set current time to `now` so we can reuse the timestamp later
    now = int(time.time())
    # Build payload
    payload = {
        'iat': now,
        # expires after 'expiry_length' seconds.
        "exp": now + 3600,
        # iss must match 'issuer' in the security definition in your
        # OpenAPI2 / API Gateway configuration. This value should be
        # service account email.
        'iss': sa_email,
        # aud must be either your endpoints service name, or match the value
        # specified as the 'x-google-audience' in the OpenAPI2 / API Gateway.
        'aud':  audience,
        # sub and email should match the service account's email address
        'sub': sa_email,
        'email': sa_email
    }
    # Sign with IAM Service Account JSON keyfile (either method works)
    # See https://google-auth.readthedocs.io/en/master/reference/google.auth.jwt.html
    # For this we can use google.auth.crypt.RSASigner or google.auth.jwt.Credentials
    # signer = google.auth.crypt.RSASigner.from_service_account_file(sa_keyfile)
    # jwt = google.auth.jwt.encode(signer, payload)
    jwt = google.auth.jwt.Credentials.from_service_account_file(
          sa_keyfile,
          audience=audience,
    )
    
    return jwt
def make_authorized_get_request(jwt_credentials, url):
    """
    Makes an authorized request to the endpoint
    :param jwt_credentials:     token
    :param url:                 request URL
    """
    headers = {
        'Authorization': 'Bearer {}'.format(jwt_credentials),
        'content-type': 'application/json'
    }
    request = None
    # Refresh the token
    jwt_credentials.refresh(request)
    # Make authorized request
    authorized_session = AuthorizedSession(jwt_credentials)
    authorized_response = authorized_session.get(url)
    return authorized_response
  
def make_authorized_post_request(jwt_credentials, url, data):
    """
    Makes an authorized POST request to the endpoint
    :param jwt_credentials:     token
    :param url:                 request URL
    :param data:                request data (JSON)
    """
    headers = {
        'Authorization': 'Bearer {}'.format(jwt_credentials),
        'content-type': 'application/json'
    }
    request = None
    # Refresh the token
    jwt_credentials.refresh(request)
    # Make authorized request
    authorized_session = AuthorizedSession(jwt_credentials)
    authorized_response = authorized_session.post(url, headers=headers, json=data)
    return authorized_response

def make_authorized_post_files_request(jwt_credentials, url, files):
    """
    Makes an authorized POST request to the endpoint
    :param jwt_credentials:     token
    :param url:                 request URL
    :param data:                request data (JSON)
    """
    headers = {
        'Authorization': 'Bearer {}'.format(jwt_credentials),
        'Access-Control-Allow-Origin': '*'
    }
    request = None
    # Refresh the token
    jwt_credentials.refresh(request)
    # Make authorized request
    authorized_session = AuthorizedSession(jwt_credentials)
    authorized_response = authorized_session.post(url, headers=headers, files=files)
    return authorized_response
