from pydantic import BaseModel
from typing import Optional

class AtorGetPost(BaseModel):
    nome: str = "Nome do ator"

class SerieGetPost(BaseModel):
    titulo: str = "Título da série"
    descricao: str = "Descrição da série"
    ano_lancamento: int = 2023
    id_categoria: int = 1

class CategoriaGetPost(BaseModel):
    nome: str = "Nome da categoria"

class MotivoAssistirGetPost(BaseModel):
    idserie: int = 1
    motivo: str = "Motivo para assistir"

#==============================================================

class AtorPutDelete(BaseModel):
    nome: Optional[str] = "Nome do ator"

class SeriePutDelete(BaseModel): #validator do pydantic
    titulo: Optional[str] = "Título da série"
    descricao: Optional[str] = "Descrição da série"
    ano_lancamento: Optional[int] = 2023
    id_categoria: Optional[int] = 1

class CategoriaPutDelete(BaseModel):
    nome: Optional[str] = "Nome da categoria"

class MotivoAssistirPutDelete(BaseModel):
    idserie: Optional[int] = 1
    motivo: Optional[str] = "Motivo para assistir"
