from fastapi.testclient import TestClient
from main import app, buscar_estoque_no_banco

client = TestClient(app)

def test_buscar_estoque_no_banco():
    """
    TESTE 1: Teste Unitário.
    Testa isoladamente se a função de buscar no SQLite está funcionando
    e retornando os dados no formato correto.
    """
    estoque = buscar_estoque_no_banco()
   
    assert isinstance(estoque, list)
    
    assert len(estoque) > 0
    
    primeiro_peixe = estoque[0]
    
    assert len(primeiro_peixe) == 2
    
    assert isinstance(primeiro_peixe[0], str)
    assert isinstance(primeiro_peixe[1], int)

def test_rota_chat_integracao():
    """
    TESTE 2: Teste de Integração.
    Testa o fluxo completo: simula um usuário enviando um POST para /chat,
    o FastAPI consultando o banco, enviando para o Gemini e devolvendo a resposta.
    """
    
    payload = {"texto": "Boa tarde, tem Pacu e Pintado?"}
    
    response = client.post("/chat", json=payload)
    
    assert response.status_code == 200
    
    dados_resposta = response.json()
    
    assert "resposta" in dados_resposta
    
    assert isinstance(dados_resposta["resposta"], str)
    assert len(dados_resposta["resposta"]) > 10