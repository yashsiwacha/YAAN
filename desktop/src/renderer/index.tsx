import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/global.css';
import moonOrb from './assets/moon-orb.png';

const favicon = document.querySelector("link[rel='icon']") || document.createElement('link');
favicon.setAttribute('rel', 'icon');
favicon.setAttribute('type', 'image/png');
favicon.setAttribute('href', moonOrb);
if (!favicon.parentElement) {
  document.head.appendChild(favicon);
}

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
