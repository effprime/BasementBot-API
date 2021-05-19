"""IPC module.
"""

import os

from discord.ext import ipc


# pylint: disable=too-few-public-methods
class IPCClient(ipc.Client):
    """Expanded IPC client."""

    async def request(self, *args, **kwargs):
        """Returns the request status code as a second element."""
        response = await super().request(*args, **kwargs)
        code = response.get("code", 200)
        return response, code


if not os.getenv("IPC_SECRET"):
    raise RuntimeError("IPC_SECRET env not found")


def get_client():
    """Generates an IPC client."""
    host = os.getenv("API_HOST") or "localhost"
    return IPCClient(host=host, secret_key=os.getenv("IPC_SECRET"))


# pylint: disable=too-few-public-methods
class SloppilyConcurrentIPCClient:
    """Client for handling concurrent requests.

    This implementation is required until discord-ext-ipc supports concurrency better.
    """

    async def request(self, *args, **kwargs):
        """Makes an IPC request utilizing an ad-hoc client instance."""
        client = get_client()
        response, code = await client.request(*args, **kwargs)
        await client.session.close()
        return response, code


# waiting on IPC clients to support concurrent requests
# ipc_client = get_client()
ipc_client = SloppilyConcurrentIPCClient()
