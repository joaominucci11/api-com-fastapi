# app/models.py
from pydantic import BaseModel
from typing import Optional


class AtorGetPost(BaseModel):
    nome: str
    personagem: str

class SerieGetPost(BaseModel):
    titulo: str
    descricao: str
    ano_lancamento: int
    id_categoria: int

class CategoriaGetPost(BaseModel):
    nome: str

class MotivoAssistirGetPost(BaseModel):
    idserie: int
    motivo: str

#===========================================================================================================================

class AtorPutDelete(BaseModel):
    nome: Optional[str] = None
    personagem: Optional[str] = None

class SeriePutDelete(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    ano_lancamento: Optional[int] = None
    id_categoria: Optional[int] = None

class CategoriaPutDelete(BaseModel):
    nome: Optional[str] = None

class MotivoAssistirPutDelete(BaseModel):
    idserie: Optional[int] = None
    motivo: Optional[str] = None
