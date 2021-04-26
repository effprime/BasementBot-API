"""Main module for the API.
"""

import os

import quart
import quart_cors
from discord.ext import ipc

if not os.getenv("IPC_SECRET"):
    raise RuntimeError("IPC_SECRET env not found")


class JSONResponse(quart.Response):
    """Response class that defaults to JSON mimetype.
    """
    default_mimetype = "application/json"


class IPCClient(ipc.Client):
    """Expanded IPC client.
    """

    async def request(self, *args, **kwargs):
        """Returns the request status code as a second element.
        """
        response = await super().request(*args, **kwargs)
        code = response.get("code", 200)
        return response, code


ipc = IPCClient(secret_key=os.getenv("IPC_SECRET"))
app = quart_cors.cors(quart.Quart(__name__))
app.response_class = JSONResponse


@app.route("/health")
async def health():
    """Runs a health check request on the bot."""
    response = await ipc.request("health")
    return response


@app.route("/describe")
async def describe():
    """Runs a describe request on the bot."""
    response = await ipc.request("describe")
    return response


@app.route("/config", methods=["GET", "PUT"])
async def config():
    """Runs a config request on the bot."""
    guild_id = quart.request.args.get("guild_id")

    if quart.request.method == "GET":
        if guild_id:
            response = await ipc.request("get_guild_config", guild_id=guild_id)
        else:
            response = await ipc.request("get_bot_config")

    if quart.request.method == "PUT":
        new_config = await quart.request.json
        response = await ipc.request(
            "edit_guild_config", guild_id=guild_id, new_config=new_config
        )

    return response


@app.route("/plugin/status")
async def plugin_status():
    """Runs a plugin status request on the bot."""
    response = await ipc.request("get_plugin_status")
    return response


@app.route("/plugin/<action>/<plugin_name>")
async def plugin_action(action, plugin_name):
    """Runs a plugin action request on the bot."""
    # clever girl
    response = await ipc.request(f"{action}_plugin", plugin_name=plugin_name)
    return response


@app.errorhandler(Exception)
async def handle_exception(exception):
    """Handles all exceptions.

    parameters:
        exception (Exception): the exception object
    """
    code = getattr(exception, "code", 500)
    return {"code": code, "error": str(exception)}, code


app.run(host="0.0.0.0", port=81)
