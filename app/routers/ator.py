from fastapi import APIRouter, HTTPException, Path
from app.database import Database
from app.models import AtorGetPost, AtorPutDelete

router = APIRouter()
db = Database()

@router.post("/ator")
def post_ator(ator: AtorGetPost):
    """
    Cadastra um novo ator no banco de dados.
    Recebe dados do ator (nome e personagem) e insere no banco de dados.
    """
    db.conectar()
    try:
        sql = "INSERT INTO ator (nome, personagem) VALUES (%s, %s)"
        params = (ator.nome, ator.personagem)
        db.executar(sql, params)
        db.connection.commit()
        return {"message": "Ator cadastrado com sucesso!"}
    except Exception as e:
        db.connection.rollback()
        raise HTTPException(status_code=500, detail=f"Erro {str(e)}")
    finally:
        db.desconectar()

@router.put("/ator/{ator_id}")
def put_ator(ator_id: int = Path(..., description="ID do ator a ser atualizado"), ator: AtorPutDelete = None):
    """
    Atualiza os dados de um ator no banco de dados.
    Recebe o ID do ator e os novos dados para atualizar.
    """
    db.conectar()
    try:
        sql_check = "SELECT * FROM ator WHERE id = %s"
        ator_existente = db.consultar(sql_check, (ator_id,))
        if not ator_existente:
            raise HTTPException(status_code=404, detail="Ator não encontrado")

        sql_update = "UPDATE ator SET nome = %s, personagem = %s WHERE id = %s"
        params = (ator.nome, ator.personagem, ator_id)
        db.executar(sql_update, params)
        db.connection.commit()

        return {"message": "Ator atualizado com sucesso!"}
    except Exception as e:
        db.connection.rollback()
        raise HTTPException(status_code=500, detail=f"Erro {str(e)}")
    finally:
        db.desconectar()

@router.delete("/ator/{ator_id}")
def delete_ator(ator_id: int = Path(..., description="ID do ator a ser deletado")):
    """
    Deleta um ator do banco de dados.
    Recebe o ID do ator e remove o registro correspondente da tabela.
    """
    db.conectar()
    try:
        # Verifica se o ator existe antes de tentar deletar
        sql_check = "SELECT * FROM ator WHERE id = %s"
        ator_existente = db.consultar(sql_check, (ator_id,))
        if not ator_existente:
            raise HTTPException(status_code=404, detail="Ator não encontrado")

        # Deleta o ator se ele existir
        sql_delete = "DELETE FROM ator WHERE id = %s"
        db.executar(sql_delete, (ator_id,))
        db.connection.commit()

        return {"message": "Ator deletado com sucesso!"}
    except Exception as e:
        # Se ocorrer algum erro, faz o rollback da transação
        db.connection.rollback()
        raise HTTPException(status_code=500, detail=f"Erro {str(e)}")
    finally:
        db.desconectar()


