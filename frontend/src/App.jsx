import { useState, useRef, useEffect } from 'react';
import Markdown from 'react-markdown';

const API_URL = 'http://localhost:8000';

function App() {
  const [messages, setMessages] = useState([
    { role: 'ai', content: 'Hello! I am your AI assistant. I have read your ebooks. Ask me anything about them!' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: userMessage }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch response');
      }

      const data = await response.json();
      setMessages(prev => [...prev, { role: 'ai', content: data.answer }]);
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, { role: 'ai', content: 'Sorry, I encountered an error. Make sure the backend and Qdrant are running.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="header">
        <h1>Knowledge Base</h1>
        <p>Chat with your personal ebook library</p>
      </div>

      <div className="chat-container">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            <Markdown>{msg.content}</Markdown>
          </div>
        ))}
        {isLoading && (
          <div className="message ai">
            <div className="typing-indicator">
              <div className="dot"></div>
              <div className="dot"></div>
              <div className="dot"></div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="input-container">
        <form onSubmit={handleSubmit} className="input-form">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question about your books..."
            disabled={isLoading}
          />
          <button type="submit" disabled={isLoading || !input.trim()}>
            Send
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;
