import base64
import datetime
from urllib.parse import urlencode
import os

import Crypto.Hash.SHA256 as SHA256
import Crypto.PublicKey.RSA as RSA
import Crypto.Signature.PKCS1_v1_5 as PKCS1_v1_5


class CloudStorageURLSigner:
    """Contains methods for generating signed URLs for Google Cloud Storage."""

    # it works because we add permission to the fs-url-signer service account
    # gsutil iam ch serviceAccount:fs-url-signer@healthshield-dev.iam.gserviceaccount.com:objectViewer gs://kmr-share/

    def __init__(self, service_account_email, private_key):
        self.key = RSA.importKey(private_key)
        self.client_id_email = service_account_email
        self.gcs_api_endpoint = "https://storage.googleapis.com"

    def _base64_sign(self, plaintext):
        """Signs and returns a base64-encoded SHA256 digest."""
        shahash = SHA256.new(plaintext.encode("latin-1"))
        signer = PKCS1_v1_5.new(self.key)
        signature_bytes = signer.sign(shahash)
        return base64.b64encode(signature_bytes)

    def _make_signature_string(self, verb, path, expiration, content_md5, content_type):
        """Creates the signature string for signing according to GCS docs."""
        signature_string = ('{verb}\n'
                            '{content_md5}\n'
                            '{content_type}\n'
                            '{expiration}\n'
                            '{resource}')
        return signature_string.format(verb=verb,
                                       content_md5=content_md5,
                                       content_type=content_type,
                                       expiration=expiration,
                                       resource=path)

    def _make_url(self, verb, path, expiration, content_type='', content_md5=''):
        """Forms and returns the full signed URL to access GCS."""
        base_url = '%s%s' % (self.gcs_api_endpoint, path)
        signature_string = self._make_signature_string(verb,
                                                       path,
                                                       expiration,
                                                       content_md5,
                                                       content_type)
        signature_signed = self._base64_sign(signature_string)
        query_params = {'GoogleAccessId': self.client_id_email,
                        'Expires': str(expiration),
                        'Signature': signature_signed}
        return base_url, query_params

    def signed_url(self, path, exp_days):
        """Performs a GET request.
        Args:
          blob: The relative API path to access, e.g. '/bucket/object'.
        """
        expiration = datetime.datetime.now() + datetime.timedelta(days=exp_days)
        expiration = int(expiration.timestamp())
        base_url, query_params = self._make_url('GET', path, expiration)
        return base_url + "?" + urlencode(query_params)
        return signed_url
