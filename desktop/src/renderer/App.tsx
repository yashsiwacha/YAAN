import React, { useState, useRef, useEffect } from 'react';
import ChatWindow from './components/ChatWindow';
import InputBar from './components/InputBar';
import Settings from './components/Settings';
import CommandCenter from './components/CommandCenter';
import './styles/App.css';

interface Message {
  id: string;
  type: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
}

const App: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [showHelp, setShowHelp] = useState(false);
  const [activeMode, setActiveMode] = useState<'chat' | 'voice'>('chat');
  const [currentView, setCurrentView] = useState<'chat' | 'command-center'>('command-center');
  const [quickSuggestions, setQuickSuggestions] = useState([
    '⏰ What time is it?',
    '✅ Show my todos',
    '💻 What is recursion?',
    '📋 Task summary',
    '😄 Tell me a joke'
  ]);
  const wsRef = useRef<WebSocket | null>(null);

  // Initialize WebSocket connection
  useEffect(() => {
    const connect = () => {
      const wsUrl = 'ws://localhost:8000/ws';
      
      try {
        const ws = new WebSocket(wsUrl);

        ws.onopen = () => {
          console.log('✅ Connected to YAAN');
          setIsConnected(true);
          wsRef.current = ws;
        };

        ws.onmessage = (event) => {
          const data = JSON.parse(event.data);
          console.log('Received:', data);
          
          setIsLoading(false);

          if (data.type === 'welcome' || data.type === 'response') {
            const message = data.message || data.text;
            const assistantMessage: Message = {
              id: Date.now().toString(),
              type: 'assistant',
              content: message,
              timestamp: new Date()
            };
            setMessages(prev => [...prev, assistantMessage]);
          }
        };

        ws.onerror = (error) => {
          console.error('WebSocket error:', error);
          const errorMessage: Message = {
            id: Date.now().toString(),
            type: 'system',
            content: 'Connection error. Please verify the backend service is running.',
            timestamp: new Date()
          };
          setMessages(prev => [...prev, errorMessage]);
        };

        ws.onclose = () => {
          console.log('❌ Disconnected from YAAN');
          setIsConnected(false);
          wsRef.current = null;
          
          const systemMessage: Message = {
            id: Date.now().toString(),
            type: 'system',
            content: 'Connection to server lost. Attempting to reconnect...',
            timestamp: new Date()
          };
          setMessages(prev => [...prev, systemMessage]);
          
          // Attempt to reconnect after 5 seconds
          setTimeout(connect, 5000);
        };

        wsRef.current = ws;
      } catch (error) {
        console.error('Failed to connect:', error);
        setIsConnected(false);
        
        setTimeout(connect, 5000);
      }
    };

    connect();

    return () => {
      wsRef.current?.close();
    };
  }, []);

  const handleSendMessage = (content: string) => {
    if (!content.trim() || !wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    // Send via WebSocket with proper format
    const data = {
      type: 'command',
      text: content
    };
    wsRef.current.send(JSON.stringify(data));
  };

  const useSuggestion = (suggestion: string) => {
    const text = suggestion.replace(/^[^a-zA-Z]+/, '').trim();
    handleSendMessage(text);
  };

  return (
    <div className="app">
      {/* Status Indicator - Always visible */}
      <div className="status-indicator">
        <div className={`status-dot ${isConnected ? 'online' : 'offline'}`}></div>
        <span className="status-text">{isConnected ? 'Online' : 'Connecting...'}</span>
      </div>

      {/* Help Button - Always visible */}
      <button className="help-btn" onClick={() => setShowHelp(!showHelp)} title="Help & Shortcuts">
        ?
      </button>

      {/* Settings Button - Always visible */}
      <button className="settings-btn" onClick={() => setShowSettings(!showSettings)} title="Settings">
        ⚙️
      </button>

      {/* Mode Toggle - Always visible */}
      <div className="mode-toggle">
        <button 
          className={`mode-btn ${currentView === 'command-center' ? 'active' : ''}`}
          onClick={() => setCurrentView('command-center')}
        >
          Dashboard
        </button>
        <button 
          className={`mode-btn ${activeMode === 'voice' && currentView !== 'command-center' ? 'active' : ''}`}
          onClick={() => { setActiveMode('voice'); setCurrentView('chat'); }}
        >
          Voice
        </button>
        <button 
          className={`mode-btn ${activeMode === 'chat' && currentView !== 'command-center' ? 'active' : ''}`}
          onClick={() => { setActiveMode('chat'); setCurrentView('chat'); }}
        >
          Chat
        </button>
      </div>

      {/* Settings Panel */}
      {showSettings && <Settings onClose={() => setShowSettings(false)} />}

      {/* Help Panel */}
      {showHelp && (
        <div className="help-panel open">
          <div className="settings-header">
            <h2>Help & Guide</h2>
            <button className="close-btn" onClick={() => setShowHelp(false)}>×</button>
          </div>
          <div className="help-section">
            <h3>💻 Coding Help</h3>
            <div className="help-examples">
              <div className="help-example">"explain this code: def hello(): print('hi')"</div>
              <div className="help-example">"what is recursion?"</div>
              <div className="help-example">"debug my Python code"</div>
            </div>
          </div>
          <div className="help-section">
            <h3>⏰ Task Management</h3>
            <div className="help-examples">
              <div className="help-example">"remind me to call John tomorrow at 3pm"</div>
              <div className="help-example">"show my todos"</div>
              <div className="help-example">"task summary"</div>
            </div>
          </div>
        </div>
      )}

      {/* Show Command Center or Chat based on view */}
      {currentView === 'command-center' ? (
        <CommandCenter />
      ) : (
        <>
          {/* Chat Mode */}
          <div className={`chat-mode ${activeMode === 'voice' ? 'hidden' : ''}`}>
            <div className="header">
              <div>
                <h1>YAAN</h1>
                <div className="header-subtitle">AI Assistant Network</div>
              </div>
            </div>
            
            <ChatWindow 
              messages={messages}
              isLoading={isLoading}
            />

            {/* Quick Suggestions */}
            {messages.length === 0 && (
              <div className="quick-suggestions">
                {quickSuggestions.map((suggestion, idx) => (
                  <button 
                    key={idx}
                    className="suggestion-btn"
                    onClick={() => useSuggestion(suggestion)}
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            )}

            {/* Typing Indicator */}
            <div className={`typing-indicator ${isLoading ? 'show' : ''}`}>
              <span>YAAN is thinking</span>
              <div className="typing-dots">
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
              </div>
            </div>
            
            <InputBar 
              onSendMessage={handleSendMessage}
              isLoading={isLoading}
              isConnected={isConnected}
              onVoiceModeClick={() => setActiveMode('voice')}
            />
          </div>

          {/* Voice Mode */}
          <div className={`voice-mode ${activeMode === 'chat' ? 'hidden' : ''}`}>
            <div className="orb-container" onClick={() => {
              const systemMessage: Message = {
                id: Date.now().toString(),
                type: 'system',
                content: 'Voice input functionality is currently in development. Please use Chat mode.',
                timestamp: new Date()
              };
              setMessages(prev => [...prev, systemMessage]);
              setTimeout(() => setActiveMode('chat'), 2000);
            }}>
              <div className="wave"></div>
              <div className="wave"></div>
              <div className="wave"></div>
              <div className="orb"></div>
            </div>
            <div className="orb-text">Click to activate voice mode</div>
            <div className="voice-hint">Voice feature is in development - Click orb for demo</div>
          </div>
        </>
      )}
    </div>
  );
};

export default App;
