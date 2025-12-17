import json
import requests


"""
Creates a key and sends an authenticated request to the token-guarded endpoint.


Run to install dependencies:
pip3 install requests

Run script:
python3 make_authenticated_request.py
"""


def create_key() -> str:
    """
    Creates a key that can access the token-guarded endpoint.
    """
    response = requests.post(
        url="http://localhost:8080/tyk/keys/create",
        headers={
            "X-Tyk-Authorization": "foo"
        },
        json={
            "access_rights": {
                "Token-Webhook": {
                    "allowed_urls": [
                        {
                        "methods": [
                            "POST"
                        ],
                        "url": "/tokenWebhook"
                        }
                    ],
                    "api_id": "Token-Webhook",
                    "api_name": "Token-Webhook",
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
            "hmac_enabled": False,
        }
    )
    print("Create key", response.status_code)
    print(response.json())

    response_json = response.json()

    return response_json.get("key")


def get_key_info(key_id) -> None:
    """Retrieves the hmac string for the key ID."""
    response = requests.get(
        url=f"http://localhost:8080/tyk/keys/{key_id}",
        headers={
            'X-Tyk-Authorization': 'foo'
        }
    )
    print("Get key info", response.status_code)
    print(json.dumps(response.json(), indent=4))


def send_authenticated_request(key_id: str) -> None:
    """
    Sends a request to the endpoint using the authorization token (key ID).
    """
    authorization_header = f'Bearer {key_id}'
    print("Authorization header", authorization_header)

    response = requests.post(
        url="http://localhost:8080/tokenWebhook",
        headers={
            "Authorization": authorization_header,
            "Content-Type": "application/json",
            "version": "Default",
        },
        json={
		"name":  "Toby",
		"email": "Toby@example.com",
        },
    )
    print(response.status_code)
    print(response.text)


key_id = create_key()
send_authenticated_request(key_id)

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
  "parsedBody": {
    "name": "Toby",
    "email": "Toby@example.com"
  }
}
"""
