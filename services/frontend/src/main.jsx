import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App.jsx";
import "./styles.css";

import { AuthProvider } from "./context/AuthContext.jsx";
import { FlashProvider } from "./context/FlashContext.jsx";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <FlashProvider>
        <AuthProvider>
          <App />
        </AuthProvider>
      </FlashProvider>
    </BrowserRouter>
  </React.StrictMode>,
);
