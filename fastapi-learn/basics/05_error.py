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
    400-499: client error (Controllable) - unlegal parameters, can't find, 
    500-599: server error (Uncontrollable) - code bug, 1/0

    async def get_res():
    r = acquire()
    try:
        yield r
    except HTTPException:
        release(r)
        raise                          # 保持原 HTTPException（通常 4xx/可控）
    except ExternalError as e:
        release(r)
        raise HTTPException(502, "Upstream failed") from e
    except Exception:
        release(r)
        raise                          # 普通/未知异常，交给兜底
    finally:
        ensure_close(r)

异常来源分三类：
- A：HTTPException（业务可预期、或你显式抛的 4xx/5xx）
- B：ExternalError → 映射成 HTTPException(502)（下游故障）
- C：其他 Exception（KeyError/ZeroDivisionError/... 未预期程序错）
'''