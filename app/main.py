from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.geral import router as geral_router
from app.database import Database

app = FastAPI(
    title="Must Watch API",              
    description="API para gerenciar séries, atores, categorias e motivos para assistir.",
    version="1.0.0"            
    )

db = Database()

app.include_router(geral_router, tags=["Endpoints"])

@app.exception_handler(404)
async def nao_encontrado(request: Request, exc: HTTPException):
    """
    Handler para erros 404 (não encontrado).
    Retorna uma mensagem personalizada quando a tabela ou recurso não é encontrado.
    """
    return JSONResponse(
        status_code=404,
        content={"message": "Nâo Encontrado"},
    )

@app.exception_handler(405)
async def metodo_nao_permitido(request: Request, exc: HTTPException):
    """
    Handler para erros 405 (método não permitido).
    Retorna uma mensagem personalizada quando o método HTTP não é permitido.
    """
    return JSONResponse(
        status_code=405,
        content={"message": "Não é permitido"},
    )

@app.exception_handler(RequestValidationError)
async def metodo_nao_valido(request, exc: RequestValidationError):
    """
    Handler para erros de validação de dados (422).
    Retorna uma mensagem de erro quando os dados passados são inválidos.
    """
    return JSONResponse(
        status_code=422,
        content={
            "message": "Não é valido",
        },
    )
