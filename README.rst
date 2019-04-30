****************************************************
Signer - the simple way to sign data and validate it
****************************************************

Usage
#####
.. code:: python

  import signer
  key = "super private key"
  signature = signer.sign(key, a="data", b="more data")
  signature1 = signer.sign(key, b="more data", a="data")

  assert signature == signature1

  signed_url = signer.sign_url(key, url="http://www.example.com/api/v8/clones?give=2", valid_for_sec=600)
  assert signer.verify_url(key, url=signed_url)
