from fastapi import FastAPI

app = FastAPI()

# the main, top-level, FastAPI application
@app.get("/app")
def read_main():
    return {"message": "Hello World from main app"}


# sub-application
subapi = FastAPI()

@subapi.get("/sub")
def read_sub():
    return {"message": "Hello World from sub API"}


# Mount the sub-application
app.mount("/subapi", subapi)