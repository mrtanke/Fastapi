from fastapi import BackgroundTasks, FastAPI, Depends
from typing import Annotated

app = FastAPI()

def write_log(message: str):
    with open("log.txt", model="w") as log:
        log.write(message)

def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q

@app.post("/send_notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks, q: Annotated[str, Depends(get_query)]):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}

'''
Suitable for small tasks, like sending notification, logging...
'''