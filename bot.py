"""Bot module.
"""

import quart
import quart_jwt_extended as jwt

import ipc

app = quart.Blueprint("bot", __name__)


@app.route("/bot/health")
async def health():
    """Runs a health check request on the bot."""
    response = await ipc.ipc_client.request("health")
    return response


@app.route("/bot/describe")
@jwt.jwt_required
async def describe():
    """Runs a describe request on the bot."""
    response = await ipc.ipc_client.request("describe")
    return response


@app.route("/bot/config", methods=["GET", "PUT"])
@jwt.jwt_required
async def config():
    """Runs a config request on the bot."""
    guild_id = quart.request.args.get("guild_id")

    if quart.request.method == "GET":
        if guild_id:
            response = await ipc.ipc_client.request(
                "get_guild_config", guild_id=guild_id
            )
        else:
            response = await ipc.ipc_client.request("get_bot_config")

    if quart.request.method == "PUT":
        new_config = await quart.request.json
        response = await ipc.ipc_client.request(
            "edit_guild_config", guild_id=guild_id, new_config=new_config
        )

    return response


@app.route("/bot/plugin/status")
@jwt.jwt_required
async def plugin_status():
    """Runs a plugin status request on the bot."""
    response = await ipc.ipc_client.request("get_plugin_status")
    return response


@app.route("/bot/plugin/<action>/<plugin_name>")
@jwt.jwt_required
async def plugin_action(action, plugin_name):
    """Runs a plugin action request on the bot."""
    # clever girl
    response = await ipc.ipc_client.request(f"{action}_plugin", plugin_name=plugin_name)
    return response
