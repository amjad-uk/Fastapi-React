from starlette.middleware.cors import CORSMiddleware
from .config import settings
cors_middleware = (CORSMiddleware, dict(allow_origins=settings.CORS_ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"], expose_headers=["X-Request-ID"],),)
