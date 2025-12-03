from fastapi import FastAPI

app = FastAPI()


@app.route("/")
def hello():
    return "Hello World!"
