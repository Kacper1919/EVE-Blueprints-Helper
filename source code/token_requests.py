import base64
import secrets
import hashlib
import urllib
from jose import jwt
import random as random_lib
import string

import requests
import webbrowser
import http.server
import socketserver

class SecurityStateDoesNotMatchException(Exception):
    pass

class NoAuthorizationCodeException(Exception):
    pass

class OAuth2CallbackHandler(http.server.SimpleHTTPRequestHandler):
            code = ''
            state = ''

            def do_GET(self):
                if '/callback' in self.path:
                    OAuth2CallbackHandler.code = self.path.split("=")[1].split("&")[0]
                    OAuth2CallbackHandler.state = self.path.split("=")[2]

                    self.server.server_close()

                return

class TokenRequester:
    def __init__(self, client_id: str,
        host: str,
        port: int,
        callback_uri: str,
        login_url: str,
        get_token_url: str,
        sso_metadata_url: str,
        jwk_audience: str,
        token_host_url: str):
          
        self.client_id: str = client_id
        self.host: str = host
        self.port: int = port
        self.callback_uri: str = callback_uri
        self.login_url: str = login_url
        self.get_token_url: str = get_token_url
        self.sso_meatadata_url: str = sso_metadata_url
        self.jwk_audience: str = jwk_audience
        self.token_host_url: str = token_host_url
        
        self.random: bytes
        self.code_challenge: str
        self.token_response: requests.Response
        self.authorization_code: str
        self.state_validator: str
        self.token_made_good: dict
        self.scopes: list
        self.token_contents: dict
        self.incomplete_token: dict
        self.complete_token: dict
    
    def troubleshoot_response_error(self, response: requests.Response) -> None:
        if response.status_code != 200:
            if response.headers.get('Content-Type').startswith('application/json'):
                print(response.json())
            print(response.request)
            print(response.request.body)
            print(response.request.url)
            print(response.request.headers)
            response.raise_for_status()

    def generate_pcke_variables(self) -> None:
        """Generate the security state and PKCE code challenge (store code_challange and random as self.variable)"""
        self.random = base64.urlsafe_b64encode(secrets.token_bytes(32))
        m = hashlib.sha256()
        m.update(self.random)
        d = m.digest()
        self.code_challenge = base64.urlsafe_b64encode(d).decode().replace("=", "")

        self.state_validator = ''.join(random_lib.choice(string.ascii_letters) for i in range(11))

    def redirect_user_to_log_in(self) -> None:
        """
        Redirect user to log in into EVE SSO with specific parameters.
        Part where user ia asked to log in into EVE.
        """
        #Assemble uri to redirect user to
        params = {
            "response_type": "code",
            "redirect_uri": self.callback_uri,
            "client_id": self.client_id,
            "scope": ' '.join([urllib.parse.quote(scp) for scp in self.scopes]),
            "state": self.state_validator,
            "code_challenge": self.code_challenge,
            "code_challenge_method": "S256"
        }

        print(f"Requesting token with scopes: {self.scopes}")

        url_args = "&".join(["{}={}".format(key, urllib.parse.quote(val)) for key, val in params.items()])
        auth_url = "{}/?{}".format(self.login_url, url_args)

        webbrowser.open(auth_url)

    def listen_to_sso_response(self) -> None:
        """
        EVE SSO wil send get request with authorization code,
        so provide server whith recieves get response from EVE SSO.
        Save authorization code from that response as self.variable.
        """

        server = socketserver.TCPServer((self.host, int(self.port)), OAuth2CallbackHandler)

        try:
            server.serve_forever()
        except OSError:
            #Everythn is good, as planned.
            pass

        server.server_close()

        if OAuth2CallbackHandler.state != self.state_validator:
            print(OAuth2CallbackHandler.state)
            print(OAuth2CallbackHandler.code)
            raise SecurityStateDoesNotMatchException
        else:
            self.authorization_code = OAuth2CallbackHandler.code

    def execute_post_request_with_authorization_code(self) -> None:
        """Send post request and recieve response with token, store it in self.variable."""
        if self.authorization_code is None or self.authorization_code == '':
            raise NoAuthorizationCodeException
        
        data = {
            "grant_type": "authorization_code",
            "code": self.authorization_code,
            "client_id": self.client_id,
            "code_verifier": self.random
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": self.token_host_url
        }

        response = requests.post(self.get_token_url, data=data, headers=headers)
        self.troubleshoot_response_error(response)
        self.incomplete_token = response.json()

    def verify_token(self) -> None:
        """Request ESI for validation"""
        jwk_algorithm = "RS256"

        sso_metadata_respnse = requests.get(self.sso_meatadata_url)
        self.troubleshoot_response_error(sso_metadata_respnse)
        sso_metadata = sso_metadata_respnse.json()

        jwks_response = requests.get(sso_metadata["jwks_uri"])
        self.troubleshoot_response_error(jwks_response)

        jwk_sets = jwks_response.json()["keys"]
        jwk_set = [item for item in jwk_sets if item["alg"] == jwk_algorithm].pop()

        jwk_issuers = (sso_metadata['issuer'], f"https://{sso_metadata['issuer']}")

        token_contents = jwt.decode(
            token = self.incomplete_token["access_token"],
            key = jwk_set,
            algorithms = jwk_set["alg"],
            issuer = jwk_issuers,
            audience = self.jwk_audience
        )

        self.complete_token = self.incomplete_token | token_contents

    def request_token(self, scopes: list) -> dict:
        self.scopes: list = scopes

        self.generate_pcke_variables()
        self.redirect_user_to_log_in()
        self.listen_to_sso_response()
        self.execute_post_request_with_authorization_code()
        self.verify_token()
        
        return self.complete_token

    def refresh_token(self, refresh_token: str) -> dict():
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": self.token_host_url
        }
        params = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.client_id
        }
        response = requests.post(self.get_token_url, headers=headers, data=params)
        self.troubleshoot_response_error(response)

        return response.json()