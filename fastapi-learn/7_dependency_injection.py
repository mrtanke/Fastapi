from typing_extensions import Annotated
from fastapi import FastAPI, Depends, Cookie, Header, HTTPException

# Dependencies with yield (little same like "return")
# Only the code prior to and including the yield statement is executed before creating a response.
app = FastAPI()

data = {
    "plumbus": {"description": "Freshly made plumbus.", "owner": "Morty"},
    "portal-gun": {"description": "Interdimensional portal gun.", "owner": "Rick"},
}

class InternalError(Exception):
    pass

def get_username():
    try:
        yield "Rick"
    except InternalError:
        print("Oops, we didn't raise again, Britney 🙈")
        raise
        
@app.get("/items/{item_id}")
def get_item(item_id: str, username: Annotated[str, Depends(get_username)]):
    if item_id == "portal-gun":
        raise InternalError(
            f'The portal gun is too dangerous to be owned by {username}!'
        )
    if item_id != "plumbus":
        raise HTTPException(
            status_code=404, detail="Item not found"
        )
    return item_id

# # Dependency in path operation decorators and global dependencies
# # This dependency will not hold return values, just validate the input
# async def verify_token(x_token: Annotated[str, Header()]):
#     if x_token != "fake-super-secret-token":
#         raise HTTPException(status_code=400, detail="X-Token header invalid")

# async def verify_key(x_key: Annotated[str, Header()]):
#     if x_key != "fake-super-secret-key":
#         raise HTTPException(status_code=400, detail="X-Key header invalid")
#     return x_key

# app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])

# @app.get("/items/")
# async def read_items():
#     return [{"item": "Foo"}, {"item": "Bar"}]

# @app.get("/users/")
# async def read_users():
#     return [{"username": "johndoe"}, {"username": "alice"}]

# #  Using dependencies with sub-dependencies and caching
# def query_extractor(q: str | None = None):
#     return q

# def query_or_cookie_extractor(
#     q: Annotated[str, Depends(query_extractor, use_cache=False)],
#     last_query: Annotated[str | None, Cookie()] = None,
# ):
#     if not q:
#         return last_query
#     return q

# @app.get("/items/")
# async def read_query(
#     query_or_default: Annotated[str, Depends(query_or_cookie_extractor)]
# ):
#     return {"q_or_cookie": query_or_default}


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