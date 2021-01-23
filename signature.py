import hashlib
import hmac
import base64

def generate_signature(query, private_key):
    message = bytes('', 'utf-8')
    secret = bytes('30bCvZwi4Tna25OJEnpUv6s7t3npfNWJxKD5HjeqYmBEKbnKBfDEjBbWELDDBUedUepSyMdGAwB4VUs2KQ==', 'utf-8')

    signature = base64.b64encode(hmac.new(secret, message, digestmod=hashlib.sha256).digest())
    return signature