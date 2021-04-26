"""IPC module.
"""

import os

from discord.ext import ipc


class IPCClient(ipc.Client):
    """Expanded IPC client."""

    async def request(self, *args, **kwargs):
        """Returns the request status code as a second element."""
        response = await super().request(*args, **kwargs)
        code = response.get("code", 200)
        return response, code


if not os.getenv("IPC_SECRET"):
    raise RuntimeError("IPC_SECRET env not found")

ipc_client = IPCClient(secret_key=os.getenv("IPC_SECRET"))
