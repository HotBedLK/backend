from ..db.transactions import Transactions
from ..exceptions.registerExceptions import credencialsNotMatchedException
from app.services.jwt import decodePasword, encodeToken
from fastapi.responses import JSONResponse


def changePasswordService(changePasswordData:dict, db):
    pass