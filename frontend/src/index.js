// Import the core React library to use JSX and React components
import React from "react";

// Import the ReactDOM library, used to render React elements into the DOM
import ReactDOM from "react-dom/client";

// Import the main CSS file for global styles (including Tailwind if used)
import './index.css';


// Import the main App component (your main UI component)
import App from './App'

// Create a root element for React to attach to
// React 18 introduced `createRoot` for concurrent rendering
const root = ReactDOM.createRoot(document.getElementById('root'))


// Render the App component inside the root DOM element
// <React.StrictMode> is a helper for highlighting potential problems in development mode
root.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);
