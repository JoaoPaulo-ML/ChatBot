from fastapi import FastAPI
import sqlite3

app = FastAPI(title="Chatbot de Pescaria - API")

#Função para retornar um unico exemplar
def buscar_estoque_no_banco():
    """Função auxiliar para conectar ao banco e buscar as linhas"""
    conexao = sqlite3.connect('pescaria.db')
    cursor = conexao.cursor()
    
    cursor.execute("SELECT id, nome, quantidade FROM estoque_peixes")
    linhas = cursor.fetchall()
    
    conexao.close()
    return linhas

#função para para retornar todos os exemplares
@app.get("/estoque")
def obter_estoque():
    
    dados_peixes = buscar_estoque_no_banco()
    
    lista_estoque = []
    for linha in dados_peixes:
        lista_estoque.append({
            "id": linha[0],
            "nome": linha[1],
            "quantidade": linha[2]
        })
    
    return lista_estoque