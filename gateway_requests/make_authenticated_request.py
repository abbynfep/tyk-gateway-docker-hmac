import base64
import datetime
import hmac
import hashlib
import json
import urllib

import requests


"""
Creates a key, retrieves the secret used to encrypt the signature, and sends an authenticated request
to the hmac-guarded endpoint.


Run to install dependencies:
pip3 install requests

Run script:
python3 make_authenticated_request.py
"""


def create_key() -> tuple[str, str]:
    """
    Creates a key that is hmac enabled.
    The hmac_string passed here is NOT the string used to encrypt the signature later.
    """
    hmac_string = "secret-key"
    response = requests.post(
        url="http://localhost:8080/tyk/keys/create",
        headers={
            "X-Tyk-Authorization": "foo"
        },
        json={
            "access_rights": {
                "carrier-webhook": {
                    "allowed_urls": [
                        {
                        "methods": [
                            "POST"
                        ],
                        "url": "/public/carrier/webhookTracking"
                        }
                    ],
                    "api_id": "carrier-webhook",
                    "api_name": "carrier-webhook",
                    "versions": [
                        "Default"
                    ]
                }
            },
            "allowance": 999,
            "rate": 1000,
            "per": 1,
            "expires": 0,
            "quota_max": -1,
            "quota_renews": 1406121006,
            "quota_remaining": 0,
            "quota_renewal_rate": 60,
            "org_id": "default",
            "hmac_enabled": True,
            "hmac_string": hmac_string,
        }
    )
    print("Create key", response.status_code)
    print(response.json())

    response_json = response.json()
    return response_json.get("key"), hmac_string


def get_key_info(key_id) -> str:
    """Retrieves the hmac string for the key ID."""
    response = requests.get(
        url=f"http://localhost:8080/tyk/keys/{key_id}",
        headers={
            'X-Tyk-Authorization': 'foo'
        }
    )
    print("Get key info", response.status_code)
    print(json.dumps(response.json(), indent=4))
    return response.json()["hmac_string"]


def send_authenticated_request(key_id: str, hmac_string: str):
    """
    I set up a tyk config for an endpoint that is guarded with hmac authorization.

    LESSONS LEARNED:
    - The secret has to be the hash retrieved from the /keys endpoint, NOT the string you sent in.
    - The clock skew has to be super high. I got a skew difference of 571 from a limit of 300. Why so high? I don't know. Maybe docker clock is a little off. I/O time from logs/prints did not seem to make a difference.
    """
    current_datetime = datetime.datetime.now(tz=datetime.timezone.utc)

    formatted_date = current_datetime.strftime("%a, %d %b %Y %H:%M:%S %Z")

    # ALTERNATIVE DATE - a UNIX timestamp.
    # formatted_date = str(int(current_datetime.timestamp()))
    print("Formatted date", formatted_date)

    # Create an HMAC object using SHA256
    # Formula from the tyk tocs: Base64Encode(HMAC-SHA1("date: Mon, 02 Jan 2006 15:04:05 MST", secret_key))
    signature_string = f"date: {formatted_date}"
    print("Signature string:")
    print(signature_string)
    print()

    hashed_signature_string = hmac.new(hmac_string.encode(), signature_string.encode(), hashlib.sha256).digest()
    base64_encoded_signature = base64.b64encode(hashed_signature_string).decode()
    url_encoded_signature = urllib.parse.quote_plus(base64_encoded_signature)

    print("Base64 encoded: ", base64_encoded_signature)
    print("URL encoded: ", url_encoded_signature)

    # Authorization header formula from the tyk documents:
    # Authorization: Signature keyId="hmac-key-1",algorithm="hmac-sha1",signature="Base64Encode(HMAC-SHA1(signing string))"
    authorization_header = f'Signature keyId="{key_id}",algorithm="hmac-sha256",headers="date",signature="{url_encoded_signature}"'
    print("Authorization header", authorization_header)

    response = requests.post(
        url="http://localhost:8080/public/carrier/webhookTracking",
        headers={
            "Date": formatted_date,
            "Authorization": authorization_header,
            "Content-Type": "application/json"
        },
        json={},
    )
    print(response.status_code)
    print(response.text)


key_id, hmac_string = create_key()
hmac_string = get_key_info(key_id)
send_authenticated_request(key_id, hmac_string)

"""
Expected result from the hmac authorization endpoint:
{
  "method": "POST",
  "protocol": "https",
  "host": "echo.free.beeceptor.com",
  "path": "/",
  "ip": "69.27.24.190:51208",
  "headers": {
    "Host": "echo.free.beeceptor.com",
    "User-Agent": "python-requests/2.32.5",
    "Content-Length": "2",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/json",
    "Date": "Tue, 09 Dec 2025 00:45:14 UTC",
    "Via": "1.1 Caddy"
  },
  "parsedQueryParams": {},
  "parsedBody": {}
}
"""
