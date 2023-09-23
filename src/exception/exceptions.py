from fastapi import HTTPException, FastAPI, Request
from fastapi.responses import JSONResponse

class IndividualException(Exception): #Собственный класс ошибок (при raise вводим параметр ошибки name)
    def __init__(self, name: str):
        self.name = name


app = FastAPI()

@app.exception_handler(IndividualException)
async def email_exception(request: Request, exc: IndividualException):
    return JSONResponse(
        status_code=501,
        content={"message" : f"{name} address dosn't exsist!"}
    )