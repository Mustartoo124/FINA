import { useChatLogic } from './hooks/useChatLogic';
import { Header } from './components/Header';
import { ChatWindow } from './components/ChatWindow';
import { ChatInput } from './components/ChatInput';
import './styles/chat.css';

function App() {
  const { messages, addMessage, deleteMessage, clearMessages } = useChatLogic();

  const handleSendMessage = (text) => {
    // Add user message
    addMessage(text, 'user');

    // Simulate assistant response after a short delay
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

  return (
    <div className="chat-container">
      <Header onClearChat={clearMessages} />
      <ChatWindow messages={messages} onDeleteMessage={deleteMessage} />
      <ChatInput onSendMessage={handleSendMessage} />
    </div>
  );
}

export default App;
