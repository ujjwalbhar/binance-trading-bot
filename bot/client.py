import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
from bot.logging_config import setup_logger

logger = setup_logger()

BASE_URL = "https://demo-fapi.binance.com"


class BinanceClient:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded"
        })

    def _sign(self, params: dict) -> dict:
        params["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        params["signature"] = signature
        return params

    def post(self, endpoint: str, params: dict) -> dict:
        signed = self._sign(params)
        url = BASE_URL + endpoint
        safe_params = {k: v for k, v in signed.items() if k != "signature"}
        logger.debug(f"POST {url} | params: {safe_params}")
        try:
            response = self.session.post(url, data=signed)
            data = response.json()
            logger.debug(f"Response [{response.status_code}]: {data}")
            if response.status_code != 200:
                raise Exception(f"API Error {data.get('code')}: {data.get('msg')}")
            return data
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Network error: {e}")
            raise
        except Exception as e:
            logger.error(f"Request failed: {e}")
            raise
