"""App setup module.
"""

import os
import traceback

import auth
import bot
import quart
import quart_cors
import quart_jwt_extended as jwt
import util

app = quart.Quart(__name__)
app.response_class = util.JSONResponse

app = quart_cors.cors(app)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET")
app.config["JWT_ERROR_MESSAGE_KEY"] = "error"

app.register_blueprint(bot.app, url_prefix="/bot/")
app.register_blueprint(auth.app, url_prefix="/auth/")

jwt_manager = jwt.JWTManager(app)


@app.errorhandler(Exception)
async def handle_exception(exception):
    """Handles all exceptions.

    parameters:
        exception (Exception): the exception object
    """
    traceback.print_exception(type(exception), exception, exception.__traceback__)

    code = getattr(exception, "code", 500)
    return {"code": code, "error": str(exception)}, code
