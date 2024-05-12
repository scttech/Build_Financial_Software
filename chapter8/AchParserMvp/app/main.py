import uvicorn
from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from .routers import files
from pydantic import ValidationError

origins = ["http://localhost:3000", "http://localhost:4000", "*"]

tags_metadata = [
    {
        "name": "ACH Files",
        "description": "Working with ACH files",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://www.google.com/",
        },
    },
]

app = FastAPI()

app.include_router(files.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of origins that should be allowed
    allow_credentials=False,  # Allows cookies to be included
    allow_methods=["*"],  # List of HTTP methods allowed for CORS
    allow_headers=["*"],  # List of HTTP headers allowed for CORS
)


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"detail": exc.errors()}
    )


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="ACH API",  # Required
        version="0.0.1",  # Required
        routes=app.routes,  # Required
        description="API for ACH file processing",
        openapi_version="3.0.0",  # Needed to fix issue with WSO2 API Manager
    )
    app.openapi_schema = openapi_schema
    app.tags_metadata = tags_metadata
    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
