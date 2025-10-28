import { useState, useEffect } from 'react';
import { useChatLogic } from './hooks/useChatLogic';
import { Header } from './components/Header';
import { ChatWindow } from './components/ChatWindow';
import { ChatInput } from './components/ChatInput';
import { EnvConfigScreen } from './components/EnvConfigScreen';
import './styles/chat.css';

function App() {
  const [configComplete, setConfigComplete] = useState(false);
  const [loading, setLoading] = useState(true);
  const { messages, addMessage, deleteMessage, clearMessages } = useChatLogic();

  useEffect(() => {
    const savedConfig = localStorage.getItem('envConfig');
    if (savedConfig) {
      setConfigComplete(true);
    }
    setLoading(false);
  }, []);

  const handleConfigComplete = (config) => {
    setConfigComplete(true);
  };

  const handleSendMessage = (text) => {
    addMessage(text, 'user');

    setTimeout(() => {
      const responses = [
        'That\'s a great message! 😊',
        'I understand what you mean.',
        'Tell me more about that.',
        'Interesting! How can I help?',
        'Got it! What else?',
        'I appreciate that! 👍',
        'Let me think about that...',
        'You\'re doing great! Keep going!',
      ];
      const randomResponse = responses[Math.floor(Math.random() * responses.length)];
      addMessage(randomResponse, 'assistant');
    }, 600);
  };

  if (loading) {
    return null;
  }

  if (!configComplete) {
    return <EnvConfigScreen onConfigComplete={handleConfigComplete} />;
  }

  return (
    <div className="chat-container">
      <Header onClearChat={clearMessages} />
      <ChatWindow messages={messages} onDeleteMessage={deleteMessage} />
      <ChatInput onSendMessage={handleSendMessage} />
    </div>
  );
}

export default App;
