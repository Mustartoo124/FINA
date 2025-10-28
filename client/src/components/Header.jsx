export function Header({ onClearChat }) {
  return (
    <header className="chat-header">
      <div className="header-content">
        <h1 className="chat-title">FINA Chat</h1>
        <button className="clear-btn" onClick={onClearChat} title="Clear all messages">
          Clear
        </button>
      </div>
    </header>
  );
}
