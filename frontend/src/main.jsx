import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";

import App from "./App.jsx";
import { AuthProvider } from "./auth/AuthContext.jsx";
import { LibraryProvider } from "./library/LibraryContext.jsx";
import "./styles/app.css";

createRoot(document.getElementById("root")).render(
  <BrowserRouter>
    <AuthProvider>
      <LibraryProvider>
        <App />
      </LibraryProvider>
    </AuthProvider>
  </BrowserRouter>
);
