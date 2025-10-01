import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    a = "a"
    b = "b" + a
    return {"hello world": b}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

'''
The main purpose of the __name__ == "__main__" is to have some code that is executed when your file is called with:
    $ python myapp.py

execution directly -> __name__ == "__main__"
imported by other module -> __name__ == module name(app.main)

How to use in Visual Studio Code:
    1. Go to the "Debug" panel.
    2. "Add configuration...".
    3. Select "Python"
    4. Run the debugger with the option "Python: Current File (Integrated Terminal)".
It will then start the server with your FastAPI code, stop at your breakpoints, etc.
'''