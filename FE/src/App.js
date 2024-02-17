import "./App.css";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import Header from "./HeaderComponent/Header";
import Home from "./HomeComponent/Home";
import Chatbot from "./ChatBot/ChatBot"
import Login from "./AuthPages/LoginPage";
import Register from "./AuthPages/RegisterPage";

import "bootstrap/dist/css/bootstrap.min.css";

import { RequireAuth, useAuthUser } from "react-auth-kit";

function App() {
  const auth = useAuthUser();

  return (
    <Router>
      <div className="App">
        <Header></Header>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route
            path="/chatbot"
            element={
              <RequireAuth loginPath="/login">
                <Chatbot />
              </RequireAuth>
            }
          />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
