import json
import typing

from aiohttp.web import middleware
from aiohttp.web_exceptions import HTTPException, HTTPUnprocessableEntity
from aiohttp_apispec.middlewares import validation_middleware

from app.web.utils import error_json_response


if typing.TYPE_CHECKING:
    from app.web.app import Application


@middleware
async def error_handling_middleware(request, handler):
    try:
        response = await handler(request)
        return response

    except HTTPUnprocessableEntity as err:
        return error_json_response(
            http_status=400,
            status='bad request',
            message=err.reason,
            data=json.loads(err.text)
        )

    except HTTPException as err:
        return error_json_response(
            http_status=err.status,
            status='error',
            message=str(err)
        )

    except Exception as err:
        return error_json_response(
            http_status=500,
            status='internal server error',
            message=str(err)
        )


def setup_middlewares(app: 'Application'):
    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(validation_middleware)
