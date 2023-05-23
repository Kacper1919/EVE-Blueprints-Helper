import os
import json
from datetime import datetime
from requests.exceptions import HTTPError
from token_requests import TokenRequester
from utils import messenger as _messenger

class NoTokensSavedException(Exception):
    pass

class TokenManager:
    def __init__(self,
        token_requester: TokenRequester,
        scopes: list,
        store_tokens: bool = True):
        
        self.token_requester: TokenRequester = token_requester
        self.scopes: list = scopes
        self.store_tokens: bool = store_tokens

        self.token: dict = {}

    def messenger(self, msg: str, _print: bool = True, pass_to_message_target: bool = False):
        _messenger(msg, _print, pass_to_message_target)

    def load_token(self) -> dict:
        if not os.path.isfile('token.json'):
            raise NoTokensSavedException
        elif os.stat("token.json").st_size == 0:
            raise NoTokensSavedException
        else:
            with open('token.json', 'r') as file:
                token = json.load(file)

        if len(token) == 0:
            raise NoTokensSavedException
        
        return token

    def save_token(self, token: dict):
        """Save token containinf of access token, refresh, sub, scopes etc"""
        with open('token.json', 'w') as file:
            json.dump(token, file, indent=4)

    def get_token(self) -> dict:
        if self.token != {}:
            previous_token = self.token
        elif self.store_tokens:
            try:
                previous_token = self.load_token()
            except NoTokensSavedException:
                previous_token = None

        if previous_token is not None:
                if 'scp' in previous_token.keys():
                    loaded_token_scopes: list = previous_token['scp']
                else:
                    loaded_token_scopes = []

                for scp in self.scopes:
                    if not scp in loaded_token_scopes:
                        self.messenger(f"Token loaded but does not hav scope: {scp}", False, True)
                        break
                else:
                    if float(previous_token['exp']) < datetime.now().timestamp() - 15.0:
                        try:
                            token = previous_token | self.token_requester.refresh_token(previous_token['refresh_token'])
                            token['exp'] = datetime.now().timestamp() + float(token['expires_in'])
                            self.messenger("Got refreshed token.", False, True)
                        except HTTPError as exception:
                            self.messenger(f"Couldn't refresh token: {exception}", False, True)
                            token = self.token_requester.request_token(self.scopes)
                            self.messenger("Got new token.", False, True)

                        if self.store_tokens:
                            self.save_token(token)

                        return token
                    else:
                        self.messenger("Got loaded token", False, True)
                        return previous_token

        self.token = self.token_requester.request_token(self.scopes)
        self.messenger("Got new token.", False, True)

        if self.store_tokens:
            self.save_token(self.token)

        return self.token