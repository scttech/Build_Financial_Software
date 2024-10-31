import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from chapter11.v1.AchParser.app.logging.audit_log import AuditLog
from chapter11.v1.AchParser.app.logging.audit_log_record import AuditLogRecord
from .routers import files, audit, companies

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

routers = [files.router, audit.router, companies.router]
for router in routers:
    app.include_router(router)

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


@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    log_message = getattr(request.state, 'log_message', "Default audit log message")
    log_record = AuditLogRecord(
        ip_address=request.client.host,
        user_agent=request.headers.get('user-agent', 'unknown'),
        http_request=request.method,
        http_response=response.status_code,
        url=str(request.url),
        message=log_message,
    )
    logger = AuditLog()
    logger.log_record(log_record)
    return response


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
