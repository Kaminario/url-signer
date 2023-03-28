import url_signer
from url_signer.gcp import CloudStorageURLSigner

def main():

    key = "super private key"
    print("process signing")
    signature = url_signer.sign(key, a="data", b="more data")
    data = {"b": "more data", "a": "data"}
    signature1 = url_signer.sign(key, **data)

    print("verify sign of the same:", signature == signature1)
    assert signature == signature1

    signed_url = url_signer.sign_url(
        key, url="http://www.example.com/api/v8/clones?give=2", valid_for_sec=600
    )

    print("verify signed_url:", url_signer.verify_url(key, url=signed_url))
    assert url_signer.verify_url(key, url=signed_url)


if __name__ == "__main__":
    main()
