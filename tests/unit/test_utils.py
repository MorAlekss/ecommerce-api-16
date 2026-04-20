import sys
sys.path.insert(0, '.')
from unittest.mock import patch, MagicMock, AsyncMock
import pytest
import httpx as httpx_mod
from src.utils.middleware import authenticated_get, authenticated_post

# src.utils.http (unit-1) not yet migrated — inject httpx on module for mock compatibility.
# After unit-1 merges, http.py will import httpx natively and this becomes a no-op.
from src.utils import http as http_module
if not hasattr(http_module, 'httpx'):
    http_module.httpx = httpx_mod


@pytest.mark.asyncio
async def test_get():
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": "value"}
    mock_response.raise_for_status.return_value = None
    with patch('src.utils.http.httpx.AsyncClient') as MockClient:
        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        MockClient.return_value = mock_client
        result = await http_module.get("https://api.example.com/test")
        assert result["data"] == "value"

@pytest.mark.asyncio
async def test_post():
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": "123"}
    mock_response.raise_for_status.return_value = None
    with patch('src.utils.http.httpx.AsyncClient') as MockClient:
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        MockClient.return_value = mock_client
        result = await http_module.post("https://api.example.com/test", {"key": "value"})
        assert result["id"] == "123"

@pytest.mark.asyncio
async def test_authenticated_get():
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": "secure"}
    mock_response.raise_for_status.return_value = None
    with patch('src.utils.middleware.httpx.AsyncClient') as MockClient:
        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        MockClient.return_value = mock_client
        result = await authenticated_get("https://api.example.com/secure", "token123")
        assert result["data"] == "secure"
