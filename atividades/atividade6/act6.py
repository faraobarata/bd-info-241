import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Criar o banco de dados SQLITE3
conn = sqlite3.connect('dbalunos.db')
cursor = conn.cursor()

# Criar a tabela TB_ALUNO
cursor.execute('''
    CREATE TABLE IF NOT EXISTS TB_ALUNO (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_nome TEXT NOT NULL,
        endereco TEXT NOT NULL
    );
''')

# Fechar a conexão
conn.close()

# Entidade Aluno
class Aluno(BaseModel):
    id: int
    aluno_nome: str
    endereco: str

# Criar a aplicação FASTAPI
app = FastAPI()

# Endpoint criar_aluno
@app.post("/alunos/")
async def criar_aluno(aluno: Aluno):
    conn = sqlite3.connect('dbalunos.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO TB_ALUNO (aluno_nome, endereco)
        VALUES (?, ?);
    ''', (aluno.aluno_nome, aluno.endereco))
    conn.commit()
    conn.close()
    return {"mensagem": "Aluno criado com sucesso"}

# Endpoint listar_alunos
@app.get("/alunos/")
async def listar_alunos():
    conn = sqlite3.connect('dbalunos.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM TB_ALUNO;
    ''')
    alunos = cursor.fetchall()
    conn.close()
    return [{"id": aluno[0], "aluno_nome": aluno[1], "endereco": aluno[2]} for aluno in alunos]

# Endpoint listar_um_aluno
@app.get("/alunos/{id}")
async def listar_um_aluno(id: int):
    conn = sqlite3.connect('dbalunos.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM TB_ALUNO
        WHERE id = ?;
    ''', (id,))
    aluno = cursor.fetchone()
    conn.close()
    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return {"id": aluno[0], "aluno_nome": aluno[1], "endereco": aluno[2]}

# Endpoint atualizar_aluno
@app.put("/alunos/{id}")
async def atualizar_aluno(id: int, aluno: Aluno):
    conn = sqlite3.connect('dbalunos.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE TB_ALUNO
        SET aluno_nome = ?, endereco = ?
        WHERE id = ?;
    ''', (aluno.aluno_nome, aluno.endereco, id))
    conn.commit()
    conn.close()
    return {"mensagem": "Aluno atualizado com sucesso"}

# Endpoint excluir_aluno
@app.delete("/alunos/{id}")
async def excluir_aluno(id: int):
    conn = sqlite3.connect('dbalunos.db')
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM TB_ALUNO
        WHERE id = ?;
    ''', (id,))
    conn.commit()
    conn.close()
    return {"mensagem": "Aluno excluído com sucesso"}