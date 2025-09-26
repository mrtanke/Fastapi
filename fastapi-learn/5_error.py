from fastapi import FastAPI, HTTPException, Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse

app = FastAPI()

# 1) 正常用法：raise HTTPException
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}

# 2) 覆盖 HTTPException 的默认处理（改为纯文本）
@app.exception_handler(StarletteHTTPException)
async def http_exc_handler(request: Request, exc: StarletteHTTPException):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

# 3) 覆盖请求校验异常，返回自定义 JSON，带回原始 body 便于调试
@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )

'''
status codes:
    100-199: information
    200-299: success
    300-399: redirection
    400-499: client error
    500-599: server error
'''