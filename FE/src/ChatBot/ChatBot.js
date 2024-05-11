import React, { useState, useEffect, useRef } from "react";
import "./ChatBot.css";
import axios from "axios";
// import botAvatar from "../../carloavatar.jpeg";
import botAvatar from "./VeritasMan.png";
import ReactMarkdown from "react-markdown";
import hljs from "highlight.js";
import "highlight.js/styles/github.css"; 

import { RequireAuth, useAuthUser } from "react-auth-kit";

function ChatBot() {
  let url = process.env.REACT_APP_API_ENDPOINT;
  const auth = useAuthUser();
  // const [messages, setMessages] = useState([]);

  const [messages, setMessages] = useState([
    { sender: "user", content: "Hello, can you explain what tokenization is?" },
    {
      sender: "Veritasense",
      content:
        "**Tokenization** is the process of breaking down text into individual units called tokens.",
    },
    {
      sender: "user",
      content:
        "Can you give examples of different tokenization methods in Python?",
    },
    {
      sender: "Veritasense",
      content:
        "**Tokenization in Python**\n\nPython provides several libraries and techniques for tokenizing text data. Here are a few popular approaches:\n\n1. **`split()` method**: The `split()` method is used to split a string into multiple substrings, separated by specified delimiters (e.g., whitespace).\n```python\ntext = 'This is an example sentence.'\ntokens = text.split()  # ['This', 'is', 'an', 'example', 'sentence.']\n```\n2. **`re` module**: The `re` (regular expression) module can be used to tokenize text using regular expressions.\n```python\nimport re\ntext = 'Hello, world! This is a test.'\ntokens = re.split(r'\\W+', text)  # ['Hello', 'world', 'This', 'is', 'a', 'test']\n```\n3. **`nltk` library**: The Natural Language Toolkit (NLTK) is a popular Python library for NLP tasks, including tokenization.\n```python\nimport nltk\ntext = 'This is an example sentence.'\ntokens = nltk.word_tokenize(text)  # ['This', 'is', 'an', 'example', 'sentence.']\n```\n4. **`spaCy` library**: SpaCy is another popular Python library for NLP tasks, including tokenization.\n```python\nimport spacy\nnlp = spacy.load('en_core_web_sm')\ntext = 'This is an example sentence.'\ntokens = [token.text for token in nlp(text)]  # ['This', 'is', 'an', 'example', 'sentence.']\n```",
    },
    { sender: "user", content: "Thanks! That was very helpful." },
    {
      sender: "Veritasense",
      content:
        "You're welcome! Feel free to ask more questions about Python or any other programming topics!",
    },
  ]);

  const [input, setInput] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [context, setContext] = useState("");
  const messagesEndRef = useRef(null);
  const [isLoading, setIsLoading] = useState(false); 
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    // Highlight all code blocks every time messages update
    document.querySelectorAll("pre code").forEach((block) => {
      hljs.highlightBlock(block);
    });
  }, [messages]);

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
    setIsLoading(true); 
    if (input.trim().length === 0) {
      setErrorMessage("Please enter your message first");
      setIsLoading(false); 
      return;
    }
    try {
      console.log("API Endpoint:", process.env.REACT_APP_API_ENDPOINT);
      const response = await axios.post(
        `${process.env.REACT_APP_API_ENDPOINT}/chat`,
        {
          message: input,
          context,
        }
      );
      setIsLoading(false);
      let messagedata = [
        {
          // sender: "Carlo Lipizzi",
          sender: "Veritasense",
          content:
            "I don't know how to respond to that, please try another question. ",
        },
      ];
      if (response.data.response.content) {
        messagedata = [
          {
            sender: "user",
            content: input,
          },
          {
            // sender: "Carlo Lipizzi",
            sender: "Veritasense",
            content: response.data.response.content,
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

  // return (
  //   <div className="chat-container">
  //     <div className="chat-messages">
  //       {messages.map((message, index) => (
  //         <div className={`chat-message-wrapper ${message.sender}`} key={index}>
  //           {message.sender === "Veritasense" && (
  //             <img src={botAvatar} alt="Bot Avatar" className="bot-avatar" />
  //           )}
  //           <div className={`chat-message ${message.sender}`}>
  //             <ReactMarkdown className="chat-message">
  //               {message.content}
  //             </ReactMarkdown>
  //           </div>
  //         </div>
  //       ))}
  //       {isLoading && (
  //         <div className="loading-animation">Generating response...</div>
  //       )}
  //       <div ref={messagesEndRef} />
  //     </div>
  //     {!isLoading && (
  //       <div className="chat-form-wrapper">
  //         {messages.length > 0 && (
  //           <button className="clear-button" onClick={clearChat}>
  //             Clear
  //           </button>
  //         )}
  //         <form onSubmit={sendMessage} className="chat-form">
  //           <textarea
  //             className="chat-input"
  //             value={input}
  //             onChange={(e) => setInput(e.target.value)}
  //             placeholder="Enter your message"
  //             disabled={isLoading}
  //             rows={Math.min(
  //               10,
  //               input.split("\n").length + Math.floor(input.length / 150)
  //             )}
  //             onKeyPress={(e) => {
  //               if (e.key === "Enter" && !e.shiftKey) {
  //                 e.preventDefault();
  //                 sendMessage(e);
  //               }
  //             }}
  //           />
  //           <button type="submit" className="send-button" disabled={isLoading}>
  //             <span className="send-symbol">➤</span>
  //           </button>
  //         </form>
  //       </div>
  //     )}
  //     {errorMessage && <p className="error-message">{errorMessage}</p>}
  //     <div className="disclaimer">
  //       <p>
  //         This is just a prototype, all information must be independently
  //         verified.
  //       </p>
  //     </div>
  //   </div>
  // );

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.map((message, index) => (
          <div className={`chat-message ${message.sender}`} key={index}>
            {message.sender === "Veritasense" && (
              <img src={botAvatar} alt="Bot Avatar" className="bot-avatar" />
            )}
            <div className="message-content">
              <ReactMarkdown>{message.content}</ReactMarkdown>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="loading-animation">Generating response...</div>
        )}
      </div>
      <div className="chat-input-area">
        <textarea
          className="chat-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter your message"
          disabled={isLoading}
        />
        <button
          className="send-button"
          onClick={sendMessage}
          disabled={isLoading || !input.trim()}
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default ChatBot;
