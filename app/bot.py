"""Bot module.
"""

import ipc
import quart
import quart_cors
import quart_jwt_extended as jwt

app = quart.Blueprint("bot", __name__)
app = quart_cors.cors(app)


@app.route("/health")
async def health():
    """Runs a health check request on the bot."""
    response = await ipc.ipc_client.request("health")
    return response


@app.route("/describe")
@jwt.jwt_required
async def describe():
    """Runs a describe request on the bot."""
    response = await ipc.ipc_client.request("describe")
    return response


@app.route("/config/main")
@jwt.jwt_required
async def main_config():
    """Runs a main config request on the bot."""
    response = await ipc.ipc_client.request("get_bot_config")
    return response


@app.route("/config/guild/<guild_id>", methods=["GET", "PUT"])
@jwt.jwt_required
async def guild_config(guild_id):
    """Runs a guild config request on the bot."""
    if quart.request.method == "GET":
        response = await ipc.ipc_client.request("get_guild_config", guild_id=guild_id)

    elif quart.request.method == "PUT":
        new_config = await quart.request.json
        response = await ipc.ipc_client.request(
            "edit_guild_config", guild_id=guild_id, new_config=new_config
        )

    return response


@app.route("/plugin/status")
@jwt.jwt_required
async def plugin_status():
    """Runs a plugin status request on the bot."""
    plugin_name = quart.request.args.get("name")
    response = await ipc.ipc_client.request(
        "get_plugin_status", plugin_name=plugin_name
    )

    return response


@app.route("/plugin/<action>/<plugin_name>")
@jwt.jwt_required
async def plugin_action(action, plugin_name):
    """Runs a plugin action request on the bot."""
    # clever girl
    response = await ipc.ipc_client.request(f"{action}_plugin", plugin_name=plugin_name)
    return response


@app.route("/guild/all")
@jwt.jwt_required
async def get_all_guilds():
    """Runs a get all guilds request on the bot."""
    response = await ipc.ipc_client.request("get_all_guilds")
    return response


@app.route("/guild/get/<guild_id>")
@jwt.jwt_required
async def get_guild(guild_id):
    """Runs a get guild request on the bot."""
    response = await ipc.ipc_client.request("get_guild", guild_id=guild_id)
    return response


@app.route("/guild/get/<guild_id>/channels")
@jwt.jwt_required
async def get_guild_channels(guild_id):
    """Runs a get guild channels request on the bot."""
    response = await ipc.ipc_client.request("get_guild_channels", guild_id=guild_id)
    return response


@app.route("/guild/leave/<guild_id>")
@jwt.jwt_required
async def leave_guild(guild_id):
    """Runs a leave guild request on the bot."""
    response = await ipc.ipc_client.request("leave_guild", guild_id=guild_id)
    return response


@app.route("/history/channel/<channel_id>")
@jwt.jwt_required
async def channel_history(channel_id):
    """Runs a channel history request on the bot."""
    limit = quart.request.args.get("limit")
    response = await ipc.ipc_client.request(
        "get_channel_message_history", channel_id=channel_id, limit=limit
    )
    return response


@app.route("/history/dm/<user_id>")
@jwt.jwt_required
async def dm_history(user_id):
    """Runs a dm history request on the bot."""
    limit = quart.request.args.get("limit")
    response = await ipc.ipc_client.request(
        "get_dm_message_history", user_id=user_id, limit=limit
    )
    return response


@app.route("/echo/user", methods=["POST"])
@jwt.jwt_required
async def echo_user():
    """Runs a echo user request on the bot."""
    data = await quart.request.json
    response = await ipc.ipc_client.request(
        "echo_user", user_id=data.get("user_id"), message=data.get("message")
    )
    return response


@app.route("/echo/channel", methods=["POST"])
@jwt.jwt_required
async def echo_channel():
    """Runs an echo channel request on the bot."""
    data = await quart.request.json
    response = await ipc.ipc_client.request(
        "echo_channel", channel_id=data.get("channel_id"), message=data.get("message")
    )
    return response
