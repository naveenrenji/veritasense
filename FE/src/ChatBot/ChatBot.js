import React, { useState, useEffect, useRef } from "react";
import "./ChatBot.css";
import axios from "axios";
// import botAvatar from "../../carloavatar.jpeg"; 
import botAvatar from "./VeritasMan.png"; 

import { RequireAuth, useAuthUser } from "react-auth-kit";

function ChatBot() {
  const auth = useAuthUser();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [context, setContext] = useState("");
  const messagesEndRef = useRef(null);
  const [isLoading, setIsLoading] = useState(false); // New state for loading animation

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    localStorage.setItem("chatMessages", JSON.stringify(messages));
    localStorage.setItem("chatContext", JSON.stringify(context));
    scrollToBottom();
  }, [messages, context]);

  const clearChat = () => {
    setMessages([]);
    setContext("");
    localStorage.removeItem("chatMessages");
    localStorage.removeItem("chatContext");
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    setIsLoading(true); // Start loading animation
    if (input.trim().length === 0) {
      setErrorMessage("Please enter your message first");
      setIsLoading(false); // Stop loading animation
      return;
    }
    try {
      const response = await axios.post("http://127.0.0.1:5000/chat", {
        message: input,
        context,
      });
      setIsLoading(false); // Stop loading animation
      let messagedata = [
        {
          // sender: "Carlo Lipizzi",
          sender: "Veritasense",
          content:
            "I don't know how to respond to that, please try another question. ",
        },
      ];
      if (response.data.response) {
        messagedata = [
          {
            sender: "user",
            content: input,
          },
          {
            // sender: "Carlo Lipizzi",
            sender: "Veritasense",
            content: response.data.response,
          },
        ];
      } else {
        messagedata = [
          {
            sender: "user",
            content: input,
          },
          ...messagedata,
        ];
      }

      setMessages([...messages, ...messagedata]);
      setInput("");
      setErrorMessage("");
    } catch (error) {
      console.error("There was an error sending the message", error);
      setErrorMessage("There was an error sending the message");
    } finally {
      setIsLoading(false); // Stop loading animation in either case
    }
  };

  return (
    <div className="chat-container">
      {/* <h1 className="chat-title">Veritasense</h1> */}
      <div className="chat-messages">
        {messages.map((message, index) => (
          <div className={`chat-message-wrapper ${message.sender}`} key={index}>
            {/* {message.sender === "Carlo Lipizzi" && (
              <img src={botAvatar} alt="Bot Avatar" className="bot-avatar" />
            )} */}
            {message.sender === "Veritasense" && (
              <img src={botAvatar} alt="Bot Avatar" className="bot-avatar" />
            )}
            <p className={`chat-message ${message.sender}`}>
              {message.content}
            </p>
          </div>
        ))}
        {isLoading && (
          <div className="loading-animation">Generating response...</div>
        )}

        <div ref={messagesEndRef} />
      </div>
      {!isLoading && (
        <div className="chat-form-wrapper">
          {messages.length > 0 && (
            <button className="clear-button" onClick={clearChat}>
              Clear
            </button>
          )}
          <form onSubmit={sendMessage} className="chat-form">
            {/* <input
            className="chat-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Enter your message"
            disabled={isLoading}
          /> */}
            <textarea
              className="chat-input"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Enter your message"
              disabled={isLoading}
              rows={Math.min(
                10,
                input.split("\n").length + Math.floor(input.length / 150)
              )}
              onKeyPress={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  sendMessage(e);
                }
              }}
            />

            <button type="submit" className="send-button" disabled={isLoading}>
              <span className="send-symbol">➤</span>
            </button>
          </form>
        </div>
      )}
      {errorMessage && <p className="error-message">{errorMessage}</p>}
      <div className="disclaimer">
        <p>
          This is just a prototype, all
          information must be independently verified.
        </p>
      </div>
    </div>
  );
}

export default ChatBot;
