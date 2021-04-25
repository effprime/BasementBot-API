"""Main module for the API.
"""

import os

import quart
from discord.ext import ipc

if not os.getenv("IPC_SECRET"):
    raise RuntimeError("IPC_SECRET env not found")

ipc = ipc.Client(secret_key=os.getenv("IPC_SECRET"))
app = quart.Quart(__name__)


@app.route("/health")
async def health():
    """Runs a health check request on the bot."""
    health_status = await ipc.request("health")
    return str(health_status)


@app.route("/describe")
async def describe():
    """Runs a describe request on the bot."""
    bot_data = await ipc.request("describe")
    return str(bot_data)


@app.route("/config")
async def config():
    """Runs a config request."""
    guild_id = quart.request.args.get("guild_id")
    config_ = await ipc.request("config", guild_id=guild_id)
    return str(config_)


app.run(host="0.0.0.0", port=81)
