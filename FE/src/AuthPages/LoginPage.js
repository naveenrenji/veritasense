import React, { useState } from "react";
import { Link, useNavigate, Navigate } from "react-router-dom";
import axios from "axios";

import "./Auth.css";

import { useSignIn } from "react-auth-kit";

export default function SignInPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  let url = process.env.REACT_APP_API_ENDPOINT;

  const signIn = useSignIn();

  const navigate = useNavigate();

  const validateEmail = () => {
    // Email validation regex pattern
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const validatePassword = () => {
    // Password validation regex pattern
    const passwordRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$/;
    return passwordRegex.test(password);
  };

  const onSignIn = async (e) => {
    e.preventDefault();
    // if (!validateEmail()) {
    //   alert("Please enter a valid Email");
    //   return;
    // }
    // if (!validatePassword()) {
    //   alert(
    //     "Please enter a password with at least 8 characters, containing at least one lowercase letter, one uppercase letter, and one number."
    //   );
    //   return;
    // }

    try {
      let body = {
        email: email,
        password: password,
      };
      console.log(process.env);
      let { data } = await axios.post(`${url}/auth/login`, body);
      if (!Object.keys(data).includes("Error")) {
        setEmail("");
        setPassword("");

        signIn({
          token: data.session_token,
          expiresIn: 3600,
          tokenType: "Bearer",
          authState: { name: data.name, email: data.email },
        });

        navigate("/chatbot");
        window.location.reload();
      } else {
        alert(data["Error"]);
        setEmail("");
        setPassword("");
      }
    } catch (e) {}
  };

  return (
    <div className="text-center m-5-auto login-form">
      <div>
        <form>
          <p>
            <label>Email address</label>
            <br />
            <input
              className="form-control"
              type="text"
              name="email"
              required
              onChange={(event) => setEmail(event.target.value)}
            />
          </p>
          <p>
            <label>Password</label>
            <br />
            <input
              className="form-control"
              type="password"
              name="password"
              required
              onChange={(event) => setPassword(event.target.value)}
            />
          </p>

          <p>
            <button
              id="sub_btn"
              className="btn btn-primary"
              onClick={onSignIn}
              type="submit"
            >
              Login
            </button>
          </p>
        </form>

        <footer>
          <p>
            First time here? <Link to="/register">Create an account</Link>
          </p>
          <p>
            <Link to="/">Back to Homepage</Link>
          </p>
        </footer>
      </div>
    </div>
  );
}
