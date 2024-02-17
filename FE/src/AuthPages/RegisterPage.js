import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import { Redirect } from "react-router-dom";

import "./Auth.css";

export default function SignUpPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [errorMessages, setErrorMessages] = useState({});

  let url = process.env.REACT_APP_API_ENDPOINT;

  const navigate = useNavigate();

  const validateName = () => {
    if (!name) throw "You must provide a name";
    if (typeof name !== "string") throw "Name must be a string";
    if (name.trim().length === 0)
      throw "Name cannot be an empty string or string with just spaces";
    let nameTrim = name.trim();
    let a = nameTrim.split(" ");
    if (a.length != 2) throw "Name must have first and last name only";
    a.forEach((element) => {
      if (!/^[a-zA-Z]+$/.test(element))
        throw "Name must contain only alphabets";
      if (element.length < 3) throw "Name must have atleast 3 letters";
    });
    return nameTrim;
  };

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

  const onSignup = async (e) => {
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
    // try {
    //   validateName(name);
    // } catch (e) {
    //   alert(e);
    //   return;
    // }

    try {
      let body = {
        name: name,
        email: email,
        password: password,
      };
      console.log(body);
      let { data } = await axios.post(`${url}/auth/signup`, body);
      if (!Object.keys(data).includes("Error")) {
        navigate("/login");
      } else {
        alert(data["Error"]);
      }
    } catch (e) {
      // const errorCode = error.code;
      // const errorMessage = error.message;
      // console.log(errorCode, errorMessage);
    }
  };

  return (
    <div className="text-center m-5-auto login-form">
      <form action="/home">
        <p>
          <label>Username</label>
          <br />
          <input
            className="form-control"
            type="text"
            name="first_name"
            required
            onChange={(event) => setName(event.target.value)}
          />
        </p>
        <p>
          <label>Email address</label>
          <br />
          <input
            className="form-control"
            type="email"
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
          <button id="sub_btn" className="btn btn-primary" onClick={onSignup}>
            Register
          </button>
        </p>
      </form>
      <footer>
        <p>
          Already have an account? <Link to="/login">Login here</Link>.
        </p>
      </footer>
    </div>
  );
}
