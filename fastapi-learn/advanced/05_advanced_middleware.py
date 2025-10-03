from fastapi import FastAPI
from fastapi.middleware import HTTPSRedirectMiddleware, TrustedHostMiddleware, GZipMiddleware

app = FastAPI()

app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com"]
)
app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=5)


@app.get("/")
async def main():
    return {"message": "Hello World"}