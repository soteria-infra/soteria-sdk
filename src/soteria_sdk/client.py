import requests

_api_key: str = ""
_api_base: str =""

def configure(api_key: str, api_base: str):
    """
    Configure the SDK with your API key and base URL.
    
    Args:
        api_key: Your API key from the web app.
        api_base: The base URL of the API service.

    Example:
        soteria.configure(
            api_key="your-api-key",
            api_base="htpps://api.soteriainfra.com"
        )
    """
    global _api_key, _api_base
    _api_key = api_key
    _api_base = api_base

def make_request(prompt: str, guard_name: str, metadata: dict) -> dict:
    """Internal function to make the API call."""
    global _api_key, _api_base
    
    if not _api_key or not _api_base:
        raise ValueError("SDK not configured. Please run soteria.configure(api_key=..., api_base=...) first.")
        
    headers = {"X-API-Key": _api_key}
    payload = {"prompt": prompt, "guard_name": guard_name, "metadata": metadata}
    
    try:
        response = requests.post(f"{_api_base}/process", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        raise ConnectionError(f"API request failed: {e.response.status_code} - {e.response.text}") from e
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Could not connect to the API service at {_api_base}. Details: {e}") from e