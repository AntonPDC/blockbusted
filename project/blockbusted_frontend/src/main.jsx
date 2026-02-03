import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";

import App from "./App.jsx";

// Your original CSS set
import "./css/index.css";
import "./css/nav.css";
import "./css/MovieList.css";
import "./css/profiles.css";
import "./css/App.css";

// New movie layout CSS
import "./css/movies_layout.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);
