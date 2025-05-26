from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.database import Database
from .models import AtorGetPost, AtorPutDelete, CategoriaGetPost, CategoriaPutDelete, MotivoAssistirGetPost, MotivoAssistirPutDelete, SerieGetPost, SeriePutDelete
#from app.routers import ator, serie, categoria, motivo_assistir

app = FastAPI()


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

@app.get('/')
def read_root():
    """
    Rota raiz. Retorna uma mensagem simples.
    """
    return {"Series": "Must Watch"}

@app.get("/{table_name}/{item_id}")
@app.get("/{table_name}")
def get_item(table_name: str, item_id: int = None):
    """
    Rota para consultar dados em uma tabela específica do banco.
    Se o `item_id` for fornecido, busca pelo ID. Caso contrário, retorna todos os itens da tabela.
    """
    db.conectar()
    tabelas_permitidas = {
        'serie': 'id',
        'categoria': 'id',
        'ator': 'id',
        'motivo_assistir': 'id',
    }
    coluna_id = tabelas_permitidas.get(table_name)

    if not coluna_id:
        raise HTTPException(status_code=404, detail="Tabela não encontrada")

    try:
        if item_id is None:
            sql = f"SELECT * FROM {table_name}"
            params = ()
        else:
            sql = f"SELECT * FROM {table_name} WHERE {coluna_id} = %s"
            params = (item_id,)

        resultado = db.consultar(sql, params)
        db.desconectar()

        if not resultado:
            raise HTTPException(status_code=404, detail="Item não encontrado")

        return resultado
    except Exception as e:
        db.desconectar()
        raise HTTPException(status_code=404, detail=f"Erro {str(e)}")


#========================================================Post=====================================================================================

@app.post("/serie")
def post_serie(serie: SerieGetPost):
    """
    Cadastra uma nova série no banco de dados.
    Recebe os dados da série (título, descrição, ano de lançamento, categoria) e insere no banco.
    """
    db.conectar()
    try:
        sql = "INSERT INTO serie (titulo, descricao, ano_lancamento, id_categoria) VALUES (%s, %s, %s, %s)"
        params = (serie.titulo, serie.descricao, serie.ano_lancamento, serie.id_categoria)
        db.executar(sql, params)
        db.connection.commit()
        return {"message": "Série cadastrada com sucesso!"}
    except Exception as e:
        db.connection.rollback()
        raise HTTPException(status_code=500, detail=f"Erro {str(e)}")
    finally:
        db.desconectar()

@app.post("/categoria")
def post_categoria(categoria: CategoriaGetPost):
    """
    Cadastra uma nova categoria no banco de dados.
    Recebe o nome da categoria e insere no banco.
    """
    db.conectar()
    try:
        sql = "INSERT INTO categoria (nome) VALUES (%s)"
        params = (categoria.nome,)
        db.executar(sql, params)
        db.connection.commit()
        return {"message": "Categoria cadastrada com sucesso!"}
    except Exception as e:
        db.connection.rollback()
        raise HTTPException(status_code=500, detail=f"Erro {str(e)}")
    finally:
        db.desconectar()

@app.post("/motivo_assistir")
def post_motivo_assistir(motivo: MotivoAssistirGetPost):
    """
    Cadastra um novo motivo de assistir uma série.
    Recebe o ID da série e o motivo, e insere no banco de dados.
    """
    db.conectar()
    try:
        sql = "INSERT INTO motivo_assistir (idserie, motivo) VALUES (%s, %s)"
        params = (motivo.idserie, motivo.motivo)
        db.executar(sql, params)
        db.connection.commit()
        return {"message": "Motivo de assistir cadastrado com sucesso!"}
    except Exception as e:
        db.connection.rollback()
        raise HTTPException(status_code=500, detail=f"Erro {str(e)}")
    finally:
        db.desconectar()


#========================================================Put======================================================================================


@app.put("/serie/{serie_id}")
def put_serie(serie_id: int = Path(..., description="ID da série a ser atualizada"), serie: SeriePutDelete = None):
    """
    Atualiza os dados de uma série no banco de dados.
    Recebe o ID da série e os novos dados para atualização.
    """
    db.conectar()
    try:
        sql_check = "SELECT * FROM serie WHERE id = %s"
        serie_existente = db.consultar(sql_check, (serie_id,))
        if not serie_existente:
            raise HTTPException(status_code=404, detail="Série não encontrada")

        sql_update = """
            UPDATE serie
            SET titulo = %s, descricao = %s, ano_lancamento = %s, id_categoria = %s
            WHERE id = %s
        """
        params = (serie.titulo, serie.descricao, serie.ano_lancamento, serie.id_categoria, serie_id)
        db.executar(sql_update, params)
        db.connection.commit()

        return {"message": "Série atualizada com sucesso!"}
    except Exception as e:
        db.connection.rollback()
        raise HTTPException(status_code=500, detail=f"Erro {str(e)}")
    finally:
        db.desconectar()

@app.put("/categoria/{categoria_id}")
def put_categoria(categoria_id: int, categoria: CategoriaPutDelete):
    """
    Atualiza os dados de uma categoria no banco de dados.
    Recebe o ID da categoria e os novos dados para atualização.
    """
    db.conectar()
    try:
        sql_check = "SELECT * FROM categoria WHERE id = %s"
        categoria_existente = db.consultar(sql_check, (categoria_id,))
        if not categoria_existente:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")

        sql_update = "UPDATE categoria SET nome = %s WHERE id = %s"
        params = (categoria.nome, categoria_id)
        db.executar(sql_update, params)
        db.connection.commit()

        return {"message": "Categoria atualizada com sucesso!"}
    except Exception as e:
        db.connection.rollback()
        raise HTTPException(status_code=500, detail=f"Erro {str(e)}")
    
@app.put("/motivo_assistir/{motivo_id}")
def put_motivo_assistir(motivo_id: int, motivo: MotivoAssistirPutDelete):
    """
    Atualiza um motivo de assistir uma série no banco de dados.
    Recebe o ID do motivo e os novos dados, e realiza a atualização no banco de dados.
    """
    db.conectar()
    try:
        # Verifica se o motivo de assistir existe antes de tentar atualizar
        sql_check = "SELECT * FROM motivo_assistir WHERE id = %s"
        motivo_existente = db.consultar(sql_check, (motivo_id,))
        if not motivo_existente:
            raise HTTPException(status_code=404, detail="Motivo de assistir não encontrado")

        # Atualiza os dados do motivo de assistir se ele existir
        sql_update = "UPDATE motivo_assistir SET idserie = %s, motivo = %s WHERE id = %s"
        params = (motivo.idserie, motivo.motivo, motivo_id)
        db.executar(sql_update, params)
        db.connection.commit()

        return {"message": "Motivo de assistir atualizado com sucesso!"}
    except Exception as e:
        # Se ocorrer algum erro, faz o rollback da transação
        db.connection.rollback()
        raise HTTPException(status_code=500, detail=f"Erro {str(e)}")
    finally:
        db.desconectar()
   

@app.delete("/serie/{serie_id}")
def delete_serie(serie_id: int = Path(..., description="ID da série a ser deletada")):
    """
    Deleta uma série do banco de dados.
    Recebe o ID da série e remove o registro correspondente da tabela.
    """
    db.conectar()
    try:
        # Verifica se a série existe antes de tentar deletar
        sql_check = "SELECT * FROM serie WHERE id = %s"
        serie_existente = db.consultar(sql_check, (serie_id,))
        if not serie_existente:
            raise HTTPException(status_code=404, detail="Série não encontrada")

        # Deleta a série se ela existir
        sql_delete = "DELETE FROM serie WHERE id = %s"
        db.executar(sql_delete, (serie_id,))
        db.connection.commit()

        return {"message": "Série deletada com sucesso!"}
    except Exception as e:
        # Se ocorrer algum erro, faz o rollback da transação
        db.connection.rollback()
        raise HTTPException(status_code=500, detail=f"Erro {str(e)}")
    finally:
        db.desconectar()

@app.delete("/categoria/{categoria_id}")
def delete_categoria(categoria_id: int = Path(..., description="ID da categoria a ser deletada")):
    """
    Deleta uma categoria do banco de dados.
    Recebe o ID da categoria e remove o registro correspondente da tabela.
    """
    db.conectar()
    try:
        # Verifica se a categoria existe antes de tentar deletar
        sql_check = "SELECT * FROM categoria WHERE id = %s"
        categoria_existente = db.consultar(sql_check, (categoria_id,))
        if not categoria_existente:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")

        # Deleta a categoria se ela existir
        sql_delete = "DELETE FROM categoria WHERE id = %s"
        db.executar(sql_delete, (categoria_id,))
        db.connection.commit()

        return {"message": "Categoria deletada com sucesso!"}
    except Exception as e:
        # Se ocorrer algum erro, faz o rollback da transação
        db.connection.rollback()
        raise HTTPException(status_code=500, detail=f"Erro {str(e)}")
    finally:
        db.desconectar()

@app.delete("/motivo_assistir/{motivo_id}")
def delete_motivo_assistir(motivo_id: int = Path(..., description="ID do motivo de assistir a ser deletado")):
    """
    Deleta um motivo de assistir uma série do banco de dados.
    Recebe o ID do motivo e remove o registro correspondente da tabela.
    """
    db.conectar()
    try:
        # Verifica se o motivo de assistir existe antes de tentar deletar
        sql_check = "SELECT * FROM motivo_assistir WHERE id = %s"
        motivo_existente = db.consultar(sql_check, (motivo_id,))
        if not motivo_existente:
            raise HTTPException(status_code=404, detail="Motivo de assistir não encontrado")

        # Deleta o motivo se ele existir
        sql_delete = "DELETE FROM motivo_assistir WHERE id = %s"
        db.executar(sql_delete, (motivo_id,))
        db.connection.commit()

        return {"message": "Motivo de assistir deletado com sucesso!"}
    except Exception as e:
        # Se ocorrer algum erro, faz o rollback da transação
        db.connection.rollback()
        raise HTTPException(status_code=500, detail=f"Erro {str(e)}")
    finally:
        db.desconectar()
