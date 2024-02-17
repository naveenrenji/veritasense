import "./Header.css";
import Container from "react-bootstrap/Container";
import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";
import {
  BrowserRouter as Router,
  Route,
  Link,
  Routes,
  useNavigate,
} from "react-router-dom";

import logoImage from "../images/logo.webp";
import { useEffect, useState } from "react";

import { withAuthUser, useAuthUser, useSignOut } from "react-auth-kit";

function Header() {
  const auth = useAuthUser();
  const signOut = useSignOut();

  const navigate = useNavigate();

  const [user, setUser] = useState("");

  const onLogout = () => {
    signOut();
    navigate("/");
  };

  useEffect(() => {
    try {
      console.log(auth().name);
      setUser(auth().name);
    } catch (e) {
      setUser("");
      console.log(e);
    }
  }, [auth()]);

  return (
    <Navbar expand="lg" className="nav-custom">
      <Container fluid>
        <Navbar.Brand className="app-title px-1" href="/">
          <img
            alt=""
            src={logoImage}
            width="30"
            height="30"
            className="d-inline-block align-top"
          />{" "}
          VeritaSense
        </Navbar.Brand>
        <Navbar.Toggle />
        <Nav.Link className="app-navs px-2" href="/chatbot">
          Chatbot
        </Nav.Link>

        <Navbar.Collapse className="justify-content-end">
          {user && (
            <Navbar.Text className="px-2">
              <Nav.Link href="/chatbot">Welcome, {user}</Nav.Link>
            </Navbar.Text>
          )}
          {!user && (
            <Navbar.Text className="px-2">
              <Link to="/login" className="btn btn-light">
                Login
              </Link>
            </Navbar.Text>
          )}
          {user && (
            <Navbar.Text className="px-2">
              <button onClick={onLogout} className="btn btn-danger logout-btn">
                Logout
              </button>
            </Navbar.Text>
          )}
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default Header;
