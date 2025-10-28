import { useEffect, useRef } from 'react';
import { MessageBubble } from './MessageBubble';

export function ChatWindow({ messages, onDeleteMessage }) {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="chat-window">
      {messages.length === 0 ? (
        <div className="empty-state">
          <p className="empty-message">No messages yet. Start a conversation!</p>
        </div>
      ) : (
        <div className="messages-list">
          {messages.map(message => (
            <MessageBubble
              key={message.id}
              message={message}
              onDelete={onDeleteMessage}
            />
          ))}
          <div ref={messagesEndRef} />
        </div>
      )}
    </div>
  );
}
