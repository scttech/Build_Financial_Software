from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from pydantic import ValidationError

# from .routers import files
from chapter6.v3.AchProcessor.app.routers import files

origins = [
    "http://localhost:3000",  # For local development
    "http://api:8000",
    # "*"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of origins (URLs) that are allowed
    allow_credentials=True,  # Allows cookies to be included
    allow_methods=["*"],  # List of HTTP methods allowed for CORS
    allow_headers=["*"],  # List of HTTP headers allowed for CORS
)

app.include_router(files.router)


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"detail": exc.errors()}
    )


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="File API",  # Required
        version="0.0.1",  # Required
        routes=app.routes,  # Required
        openapi_version="3.0.0",  # Needed to fix issue with WSO2 API Manager
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
