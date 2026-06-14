import pytest
import mock
import aiohttp

from custom_components.octopus_energy.api_client import OctopusEnergyApiClient, TimeoutException

@pytest.mark.asyncio
@pytest.mark.parametrize("client_error",[
  aiohttp.ClientConnectionError(),
  aiohttp.ClientOSError(),
  aiohttp.ServerDisconnectedError(),
])
async def test_when_token_fetch_raises_connection_error_then_timeout_exception_raised(client_error):
  # Arrange
  client = OctopusEnergyApiClient("NOT_REAL")

  async def async_mocked_fetch_token(*args, **kwargs):
    raise client_error

  # Act
  with mock.patch.multiple(OctopusEnergyApiClient, _OctopusEnergyApiClient__async_fetch_token=async_mocked_fetch_token):
    try:
      await client.async_refresh_token()
      assert False
    except TimeoutException:
      assert True
