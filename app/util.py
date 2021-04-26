"""Utils module.
"""

import quart


class JSONResponse(quart.Response):
    """Response class that defaults to JSON mimetype."""

    default_mimetype = "application/json"
