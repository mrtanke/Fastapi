from typing import Annotated
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

@app.post("/files/")
async def create_files(files: Annotated[list[bytes], File(description="Multiple files as bytes")]):
    return {"file_sizes": [len(file) for file in files]}

@app.post("/uploadfile/")
async def create_upload_files(files: Annotated[list[UploadFile], File(description="Multiple files as UploadFile")]):
    return {"filenames": [file.filename for file in files]}

@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfile/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)