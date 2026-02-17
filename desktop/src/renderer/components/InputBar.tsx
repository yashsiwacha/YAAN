import React, { useState, useRef } from 'react';
import '../styles/InputBar.css';

interface InputBarProps {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
  isConnected: boolean;
  voiceMode: boolean;
}

const InputBar: React.FC<InputBarProps> = ({
  onSendMessage,
  isLoading,
  isConnected,
  voiceMode
}) => {
  const [input, setInput] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);

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

  const handleVoiceClick = async () => {
    if (!voiceMode) return;

    if (isRecording) {
      mediaRecorderRef.current?.stop();
      setIsRecording(false);
    } else {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const mediaRecorder = new MediaRecorder(stream);

        const audioChunks: Blob[] = [];

        mediaRecorder.ondataavailable = (e) => {
          audioChunks.push(e.data);
        };

        mediaRecorder.onstop = () => {
          const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
          // Here you would typically send the audio to the backend for transcription
          console.log('Audio recorded:', audioBlob);
          stream.getTracks().forEach(track => track.stop());
        };

        mediaRecorder.start();
        mediaRecorderRef.current = mediaRecorder;
        setIsRecording(true);
      } catch (err) {
        console.error('Microphone access denied:', err);
      }
    }
  };

  return (
    <div className="input-bar">
      {!isConnected && (
        <div className="connection-warning">
          ⚠️ Not connected to backend. Check your connection.
        </div>
      )}
      <div className="input-container">
        {voiceMode && (
          <button
            className={`voice-record-btn ${isRecording ? 'recording' : ''}`}
            onClick={handleVoiceClick}
            disabled={!voiceMode}
            title={isRecording ? 'Stop recording' : 'Start recording'}
          >
            {isRecording ? '⏹️' : '🎙️'}
          </button>
        )}

        <textarea
          ref={inputRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={voiceMode ? 'Speak or type...' : 'Type your message... (Shift+Enter for new line)'}
          disabled={!isConnected}
          rows={3}
          className="input-field"
        />

        <button
          onClick={handleSend}
          disabled={!input.trim() || isLoading || !isConnected}
          className="send-btn"
          title="Send message (Enter)"
        >
          {isLoading ? '⏳' : '📤'}
        </button>
      </div>
    </div>
  );
};

export default InputBar;
