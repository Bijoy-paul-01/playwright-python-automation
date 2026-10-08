"""Reusable REST API Client wrapping requests for API testing."""
from typing import Any, Dict, Optional
import requests
from config.config import API_BASE_URL, API_TIMEOUT_SECONDS

class APIClient:
    """Wrapper around requests.Session providing standard HTTP methods and error handling."""

    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json",
        })
        self.timeout = API_TIMEOUT_SECONDS

    def _build_url(self, endpoint: str) -> str:
        """Constructs full URL from endpoint."""
        cleaned_endpoint = endpoint.lstrip("/")
        return f"{self.base_url}/{cleaned_endpoint}"

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """Sends a GET request."""
        url = self._build_url(endpoint)
        return self.session.get(url, params=params, timeout=self.timeout, **kwargs)

    def post(self, endpoint: str, json: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """Sends a POST request."""
        url = self._build_url(endpoint)
        return self.session.post(url, json=json, timeout=self.timeout, **kwargs)

    def put(self, endpoint: str, json: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """Sends a PUT request."""
        url = self._build_url(endpoint)
        return self.session.put(url, json=json, timeout=self.timeout, **kwargs)

    def patch(self, endpoint: str, json: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """Sends a PATCH request."""
        url = self._build_url(endpoint)
        return self.session.patch(url, json=json, timeout=self.timeout, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """Sends a DELETE request."""
        url = self._build_url(endpoint)
        return self.session.delete(url, timeout=self.timeout, **kwargs)
