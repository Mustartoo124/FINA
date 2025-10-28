export function MessageBubble({ message, onDelete }) {
  const isUser = message.sender === 'user';

  return (
    <div className={`message-container ${isUser ? 'user-message' : 'assistant-message'}`}>
      <div className="message-bubble">
        <p className="message-text">{message.text}</p>
        <span className="message-time">{message.timestamp}</span>
      </div>
      {isUser && (
        <button
          className="delete-btn"
          onClick={() => onDelete(message.id)}
          title="Delete message"
          aria-label="Delete message"
        >
          ×
        </button>
      )}
    </div>
  );
}
