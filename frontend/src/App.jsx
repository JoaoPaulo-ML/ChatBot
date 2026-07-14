import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  // Guarda o histórico de mensagens do chat
  const [mensagens, setMensagens] = useState([
    { texto: "Olá! Sou o assistente da Peixaria Pantaneira. Como posso te ajudar com nosso estoque hoje?", enviadaPor: "bot" }
  ]);
  // Guarda o texto que o usuário está digitando no input
  const [inputUsuario, setInputUsuario] = useState("");
  // Controla se o bot está pensando/carregando a resposta
  const [carregando, setCarregando] = useState(false);

  // Referência para fazer o chat rolar para baixo automaticamente a cada nova mensagem
  const fimDoChatRef = useRef(null);

  const rolarParaBaixo = () => {
    fimDoChatRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    rolarParaBaixo();
  }, [mensagens, carregando]);

  const enviarMensagem = async (e) => {
    e.preventDefault();
    if (!inputUsuario.trim()) return;

    const mensagemDoUsuario = inputUsuario;
    setInputUsuario(""); // Limpa o campo de texto

    // 1. Adiciona a mensagem do usuário no chat
    setMensagens((prev) => [...prev, { texto: mensagemDoUsuario, enviadaPor: "usuario" }]);
    setCarregando(true);

    try {
      // 2. Faz a chamada para o nosso backend FastAPI
      const respostaAPI = await axios.post("http://127.0.0.1:8000/chat", {
        texto: mensagemDoUsuario
      });

      // 3. Adiciona a resposta do Gemini no chat
      setMensagens((prev) => [...prev, { texto: respostaAPI.data.resposta, enviadaPor: "bot" }]);
    } catch (error) {
      console.error("Erro ao falar com o bot:", error);
      setMensagens((prev) => [
        ...prev,
        { texto: "Ops! Tive um problema para me conectar ao estoque. Tente novamente em breve, companheiro!", enviadaPor: "bot" }
      ]);
    } finally {
      setCarregando(false);
    }
  };

  return (
    <div className="container-app">
      <header className="cabecalho">
        <h1>🐟 Peixaria Corumbá</h1>
        <p>Estoque em Tempo Real - Chatbot Pantaneiro</p>
      </header>

      <div className="area-chat">
        {mensagens.map((msg, index) => (
          <div key={index} className={`balao-container ${msg.enviadaPor === 'usuario' ? 'usuario-alinhamento' : 'bot-alinhamento'}`}>
            <div className={`balao ${msg.enviadaPor === 'usuario' ? 'balao-usuario' : 'balao-bot'}`}>
              {msg.texto}
            </div>
          </div>
        ))}
        {carregando && (
          <div className="balao-container bot-alinhamento">
            <div className="balao balao-bot carregando">
              Digitando... 🎣
            </div>
          </div>
        )}
        <div ref={fimDoChatRef} />
      </div>

      <form onSubmit={enviarMensagem} className="formulario-envio">
        <input
          type="text"
          value={inputUsuario}
          onChange={(e) => setInputUsuario(e.target.value)}
          placeholder="Pergunte sobre Pacu, Pintado, Dourado..."
          disabled={carregando}
        />
        <button type="submit" disabled={carregando}>Enviar</button>
      </form>
    </div>
  );
}

export default App;