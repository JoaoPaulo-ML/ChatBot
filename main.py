from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

CHAVE_API = os.getenv("GEMINI_API_KEY")

app = FastAPI(title="Chatbot de Pescaria - API")

client = genai.Client(api_key=CHAVE_API)

class Mensagem(BaseModel):
    texto: str

# Abre o SQLite, pega a lista atualizada de peixes (nome e quantidade) e fecha a conexão com segurança.
def buscar_estoque_no_banco():
    """Conecta à base de dados e devolve as linhas com o nome e quantidade"""
    conexao = sqlite3.connect('pescaria.db')
    cursor = conexao.cursor()
    cursor.execute("SELECT nome, quantidade FROM estoque_peixes")
    linhas = cursor.fetchall()
    conexao.close()
    return linhas

# Pega os dados brutos obtidos pela função anterior e os entrega formatados (JSON) para consulta rápida no navegador.
@app.get("/estoque")
def obter_estoque():
    """Rota para verificar rapidamente o stock cru no navegador"""
    dados_peixes = buscar_estoque_no_banco()
    lista_estoque = [{"nome": linha[0], "quantidade": linha[1]} for linha in dados_peixes]
    return lista_estoque

# Recebe a pergunta do cliente, busca o estoque real do banco, envelopa tudo num roteiro de instruções e envia para o Gemini responder com carisma pantaneiro.
@app.post("/chat")
def conversar_com_bot(mensagem: Mensagem):
    """Rota principal que faz a ponte entre o cliente, a base de dados e o Gemini"""
    
    estoque = buscar_estoque_no_banco()
    
    texto_estoque = ", ".join([f"{nome}: {qtd}" for nome, qtd in estoque])
    
    prompt_sistema = f"""
    És um assistente virtual amigável de uma peixaria/loja de pesca na região de Corumbá/MS, no Pantanal.
    O cliente quer saber sobre o nosso stock de peixes. 
    Responde à pergunta do cliente usando EXCLUSIVAMENTE a seguinte informação de stock atual: 
    {texto_estoque}.
    Seja educado e podes adicionar um ligeiro toque pantaneiro na resposta.
    
    Pergunta do cliente: {mensagem.texto}
    """
   
    try:
        resposta = client.models.generate_content(
            model='gemini-3.5-flash', 
            contents=prompt_sistema
        )
        return {"resposta": resposta.text}
    
    except Exception as e:
        
        raise HTTPException(status_code=500, detail=str(e))