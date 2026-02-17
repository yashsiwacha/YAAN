import React from 'react';
import '../styles/InputBar.css';
interface InputBarProps {
    onSendMessage: (message: string) => void;
    isLoading: boolean;
    isConnected: boolean;
    voiceMode: boolean;
}
declare const InputBar: React.FC<InputBarProps>;
export default InputBar;
