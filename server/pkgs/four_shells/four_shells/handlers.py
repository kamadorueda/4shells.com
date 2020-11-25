"""Application route handlers."""

# Third party libraries
from authlib.integrations.starlette_client import (
    OAuth,
)
from starlette.requests import (
    Request,
)
from starlette.responses import (
    Response,
)
from starlette.schemas import (
    SchemaGenerator,
)

# Local libraries
from four_shells import (
    config,
)

# Constants
OAUTH = OAuth()
OAUTH.register(
    name='google',
    client_id=config.GOOGLE_OAUTH_CLIENT_ID_SERVER,
    client_secret=config.GOOGLE_OAUTH_SECRET_SERVER,
    server_metadata_url=(
        'https://accounts.google.com/.well-known/openid-configuration'
    ),
    client_kwargs={
        'scope': 'email'
    },
)
SCHEMA = SchemaGenerator({
    "openapi": "3.0.0",
    "info": {
        "title": "Four Shells",
    },
})


async def on_shutdown() -> None:
    """Server shutdown script."""


async def on_startup() -> None:
    """Server startup script."""


def index(request: Request) -> Response:
    return config.TPL.TemplateResponse('react.html', {
        'css': config.from_cdn('/static/index.css'),
        'js': config.from_cdn('/static/index.js'),
        'request': request,
    })


async def oauth_google_init(request: Request) -> Response:
    return await OAUTH.google.authorize_redirect(
        request,
        request.url_for('oauth_google_receive'),
    )


async def oauth_google_receive(request: Request) -> Response:
    token = await OAUTH.google.authorize_access_token(request)
    data = await OAUTH.google.parse_id_token(request, token)

    request.session['email'] = data['email']

    return Response(f'{data}')


async def ping(request: Request) -> Response:
    """
    responses:
      200:
        description: Ping the server in order to perform a health check.
    """
    return Response()


def schema(request: Request) -> Response:
    response = SCHEMA.OpenAPIResponse(request)
    return Response(response.body, media_type='text/plain')
