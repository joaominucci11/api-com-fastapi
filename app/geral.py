from typing import Union
from fastapi import APIRouter, HTTPException
from app.database import Database
from app.models import AtorGetPost, AtorPutDelete, CategoriaGetPost, CategoriaPutDelete, SerieGetPost, SeriePutDelete

router = APIRouter()
db = Database()

@router.get('/')
def read_root():
    """
    Rota raiz. Retorna uma mensagem simples.
    """
    return {"Series": "Must Watch"}

@router.get("/{table_name}")
def get_item(table_name: str = None, item_id: int = None):
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


@router.post("/{table_name}")
def post_item(table_name: str, item: Union[AtorGetPost, CategoriaGetPost, SerieGetPost]):
    tabelas_modelos = {
        'ator': AtorGetPost,
        'categoria': CategoriaGetPost,
        'serie': SerieGetPost,
    }

    if table_name not in tabelas_modelos:
        raise HTTPException(status_code=404, detail="Tabela não permitida")

    db.conectar()

    try:
        if table_name == 'ator':
            sql = "INSERT INTO ator (nome) VALUES (%s)"
            params = (item.nome,)
        elif table_name == 'categoria':
            sql = "INSERT INTO categoria (nome) VALUES (%s)"
            params = (item.nome,)
        elif table_name == 'serie':
            sql = "INSERT INTO serie (nome, descricao, ano_lancamento, id_categoria) VALUES (%s, %s, %s, %s)"
            params = (item.nome, item.descricao, item.ano_lancamento, item.id_categoria)

        db.executar(sql, params)
        db.connection.commit()
        return {"message": f"{table_name.capitalize()} cadastrado com sucesso!"}
    except Exception as e:
        db.connection.rollback()
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")
    finally:
        db.desconectar()

@router.put("/{table_name}/{item_id}")
def put_item(table_name: str, item_id: int, item: Union[AtorGetPost, CategoriaGetPost, SerieGetPost]):
    """
    Atualiza um item existente (ator, categoria, motivo_assistir, serie) no banco de dados.
    A tabela e os dados serão passados dinamicamente, assim como o ID.
    """
    tabelas_modelos = {
        'ator': AtorPutDelete,
        'categoria': CategoriaPutDelete,
        'serie': SeriePutDelete,
    }

    if table_name not in tabelas_modelos:
        raise HTTPException(status_code=404, detail="Tabela não permitida")

    db.conectar()

    try:
        if table_name == 'ator':
            sql = "UPDATE ator SET nome = %s WHERE id = %s"
            params = (item.nome, item_id)
        elif table_name == 'categoria':
            sql = "UPDATE categoria SET nome = %s WHERE id = %s"
            params = (item.nome, item_id)
        elif table_name == 'serie':
            sql = "UPDATE serie SET nome = %s, descricao = %s, ano_lancamento = %s, id_categoria = %s WHERE id = %s"
            params = (item.nome, item.descricao, item.ano_lancamento, item.id_categoria, item_id)

        db.executar(sql, params)
        db.connection.commit()

        return {"message": f"{table_name.capitalize()} atualizado com sucesso!"}
    except Exception as e:
        db.connection.rollback()
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")
    finally:
        db.desconectar()

@router.delete("/{table_name}/{item_id}")
def delete_item(table_name: str, item_id: int):
    """
    Deleta um item (ator, categoria, motivo_assistir, serie) do banco de dados.
    A tabela e o ID do item serão passados dinamicamente.
    """
    tabelas_permitidas = {
        'ator': 'id',
        'categoria': 'id',
        'serie': 'id',
    }

    if table_name not in tabelas_permitidas:
        raise HTTPException(status_code=404, detail="Tabela não permitida")

    db.conectar()

    try:
        coluna_id = tabelas_permitidas[table_name]
        sql = f"DELETE FROM {table_name} WHERE {coluna_id} = %s"
        params = (item_id,)

        db.executar(sql, params)
        db.connection.commit()

        return {"message": f"{table_name.capitalize()} excluído com sucesso!"}
    except Exception as e:
        db.connection.rollback()
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")
    finally:
        db.desconectar()