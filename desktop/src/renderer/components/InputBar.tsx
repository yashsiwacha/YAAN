import React, { useState, useRef } from 'react';
import '../styles/InputBar.css';

interface InputBarProps {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
  isConnected: boolean;
  onVoiceModeClick: () => void;
}

const InputBar: React.FC<InputBarProps> = ({
  onSendMessage,
  isLoading,
  isConnected,
  onVoiceModeClick
}) => {
  const [input, setInput] = useState('');
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const handleSend = () => {
    if (input.trim() && !isLoading && isConnected) {
      onSendMessage(input);
      setInput('');
      inputRef.current?.focus();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleVoiceClick = () => {
    onVoiceModeClick();
  };

  return (
    <div className="input-area">
      <input
        ref={inputRef as any}
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown as any}
        placeholder="Type your message..."
        disabled={!isConnected}
        className="input-field"
      />

      <button
        className="btn btn-voice"
        onClick={handleVoiceClick}
        disabled={!isConnected}
        title="Voice input"
      >
        Voice
      </button>

      <button
        onClick={handleSend}
        disabled={!input.trim() || isLoading || !isConnected}
        className="btn btn-send"
        title="Send message"
      >
        Send
      </button>
    </div>
  );
};

export default InputBar;
