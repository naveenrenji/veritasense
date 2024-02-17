import "./ChatbotPage.css";

import React, { useState, useContext, useEffect, useRef } from "react";
import axios from "axios";

import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Badge from "react-bootstrap/Badge";
import ListGroup from "react-bootstrap/ListGroup";

import { RequireAuth, useAuthUser } from "react-auth-kit";

import { useIdleTimer } from "react-idle-timer/legacy";

// let allMessages = [];
let greetings = {
  "hi ": "Hello there!",
  "hello ": "Hello there!",
  "hey ": "Hello there!",
  "helloo ": "Hello there!",
  "hellooo ": "Hello there!",
  "g morining": "Good morning",
  "gmorning ": "Good morning",
  "good morning": "Good morning",
  "morning ": "Good morning",
  "good day": "Good day mate",
  "good afternoon": "Good afternoon",
  "good evening": "Good evening",
  "greetings ": "Hello there!",
  "greeting ": "Hello there!",
  "good to see you": "It's good to see you too!",
  "its good seeing you": "It's good to see you too!",
  "how are you":
    "I'm doing well, thank for asking. I hope you are doing well too.",
  "how're you":
    "I'm doing well, thank for asking. I hope you are doing well too.",
  "how are you doing":
    "I'm doing well, thank for asking. I hope you are doing well too.",
  "how ya doin'":
    "I'm doing well, thank for asking. I hope you are doing well too.",
  "how ya doin":
    "I'm doing well, thank for asking. I hope you are doing well too.",
  "how is everything":
    "I'm doing well, thank for asking. I hope you are doing well too.",
  "how is everything going":
    "I'm doing well, thank for asking. I hope you are doing well too.",
  "how's everything going":
    "I'm doing well, thank for asking. I hope you are doing well too.",
  "how is you":
    "I'm doing well, thank for asking. I hope you are doing well too.",
  "how's you":
    "I'm doing well, thank for asking. I hope you are doing well too.",
  "how are things":
    "I'm doing well, thank for asking. I hope you are doing well too.",
  "how're things":
    "I'm doing well, thank for asking. I hope you are doing well too.",
  "how is it going":
    "I'm doing well, thank for asking. I hope you are doing well too.",
  "how's it going":
    "I'm doing well, thank for asking. I hope you are doing well too.",
  "how's it goin'":
    "I'm doing well, thank for asking. I hope you are doing well too.",
  "how's it goin":
    "I'm doing well, thank for asking. I hope you are doing well too.",
  "g’day ": "g'day to you too!",
  "howdy ": "Howdy mate!",
};

const fillerWords = [
  "cool",
  "sounds good",
  "okay",
  "ok",
  "k",
  "right",
  "alright",
  "I'll do it",
  "understood",
  "got it",
  "sure",
  "fine",
  "yes",
  "no problem",
  "certainly",
  "absolutely",
  "definitely",
  "of course",
  "clear",
  "agreed",
  "I see",
  "makes sense",
  "understandable",
  "fair enough",
  "I get it",
  "I understand",
  "perfect",
  "great",
  "excellent",
  "wonderful",
  "fantastic",
  "awesome",
  "nice",
  "interesting",
  "amazing",
  "good idea",
  "I agree",
  "I concur",
  "indeed",
  "precisely",
  "true",
  "that's right",
  "correct",
  "I follow",
  "I comprehend",
  "acknowledged",
  "noted",
  "I'm on it",
  "I can do that",
  "will do",
  "I'm with you",
  "I'm there",
  "I'm ready",
  "let's go",
  "let's do it",
  "bring it on",
  "you got it",
  "no worries",
  "no doubt",
  "for sure",
  "you bet",
  "absolutely",
  "most definitely",
  "without a doubt",
  "count me in",
  "I'm in",
  "sign me up",
  "let's roll",
  "rock on",
  "keep going",
  "go on",
  "continue",
  "proceed",
  "carry on",
  "keep it up",
  "good to go",
  "ready when you are",
  "I'm prepared",
  "all set",
  "ready to go",
  "go ahead",
  "lead the way",
  "after you",
  "I'm listening",
  "I'm all ears",
  "speak on",
  "tell me more",
  "I'm intrigued",
  "that's fascinating",
  "very well",
  "as you say",
  "if you say so",
  "I'll trust you",
  "I believe you",
  "I'm convinced",
  "you're the boss",
  "you're in charge",
  "you lead",
  "I follow",
  "you command",
  "I'll heed",
  "I'll adhere",
  "I'll stick to it",
  "I'm on board",
  "I'm game",
  "sounds like a plan",
  "sounds like a deal",
  "sounds promising",
  "that works",
  "that's acceptable",
  "that's okay",
  "that's fine",
  "that'll do",
  "that suits me",
  "that's agreeable",
  "that's adequate",
  "that's sufficient",
  "that's up to par",
  "that meets expectations",
  "that's satisfactory",
  "that's decent",
  "that's good enough",
  "that's passable",
  "that's tolerable",
  "I can live with that",
  "I can work with that",
  "I can manage that",
  "I can handle that",
  "I can deal with that",
  "I'm comfortable with that",
  "I'm content with that",
  "I'm satisfied with that",
  "I'm happy with that",
  "that's all right",
  "that's all good",
  "it's all good",
  "it's fine",
  "it's okay",
  "it's alright",
  "it's acceptable",
  "it's decent",
  "it's satisfactory",
  "it's sufficient",
  "it's adequate",
  "it's up to standard",
  "it's up to snuff",
  "it meets the mark",
  "it hits the spot",
  "it does the trick",
  "it works for me",
  "it's suitable",
  "it's fitting",
  "it's appropriate",
  "it's proper",
  "it's correct",
  "it's just right",
  "it's spot on",
  "it's on point",
  "it's on the money",
  "it's on target",
  "it's on the nose",
  "it's on the mark",
  "it's on the button",
  "it's just what I needed",
  "it's just what I wanted",
  "it's just what I was looking for",
  "it's just the ticket",
  "it's just the thing",
  "it's the answer",
  "it's the solution",
  "it's the remedy",
  "it's the cure",
  "it's the fix",
  "it's the way to go",
  "it's the right choice",
  "it's the best option",
  "it's the ideal choice",
  "it's the perfect choice",
  "it's the optimal choice",
  "it's the preferable choice",
  "it's the choice for me",
];

const botIntro = [
  {
    sender: "bot",
    content:
      "Hello! My name is Aida. I am here to help you design the next generation of sustainable washing machines.",
  },
  {
    sender: "bot",
    content:
      "I will need you to describe your idea on a new and innovative, but feasible washing machine.",
  },
  {
    sender: "bot",
    content: "Please describe your idea/design using complete sentences.",
  },
];
const chatbotFailMessage = {
  sender: "bot",
  content: "The chatbot is offline right now, please try again in sometime",
};

const validityPassMessage = "Alright, let me analyze your description now.";
const validityFailMessages = [
  "Your input is not recognized as a valid washing machine design. Please try to make more specific descriptions about washing machine design.",
  "It’s still not quite relevant to washing machines. Here's an example of the design idea: “The machine is manufactured from parts that generate less electronic waste and is easy to take apart and recycle.” Please try again.",
  "Unfortunately, the input seems irrelevant to washing machine design.",
];

const noveltyPassMessage =
  "Your idea is indeed innovative! This idea has the potential to bring novel perspectives to the design field.";
const noveltyFailMessages = [
  "The idea is robust, but similar concepts have been explored in the past. You may consider using different methodologies, materials, or technologies. Please try again.",
  "The idea still lacks uniqueness. Have you considered pivoting the idea’s focus? Here is an example” Sense the load automatically and automatically determine the time to wash”. Please elaborate the idea or brainstorm another one.",
  "Thanks for your effort. There are some notions similar to the one you proposed.",
];

const feasibilityPassMessage =
  "Your idea appears to be quite feasible. You're on the right path to creating a successful design.";
const feasibilityFailMessages = [
  "It may be challenging in executing this idea. Please provide more details or propose a more feasible idea.",
  "The feasibility still seems to be a concern. Here is an example of the feasible design idea: “The machine is manufactured from parts that generate less electronic waste and are easy to take apart and recycle.” Please elaborate the idea or brainstorm another one.",
  "Thanks for your effort. Unfortunately, the idea seems infeasible given the current technology.",
];

// const overallPassMessage =
//   "Fantastic work so far! Together, we've refined your design until it's both novel and feasible. Thank you for using the Engineering Design Evaluation Chatbot.";
// const overallFailMessage =
//   "Thank you for your efforts. While the design didn't meet all the criteria this time, don't be discouraged. Keep iterating and come back when you're ready.";

const feedbackMessage = [
  "Thank you for participating in this design task. Please share your valuable feedback on your experience by filling out the survey",
  "https://thesse.qualtrics.com/jfe/form/SV_6l4fcCKTfiVdyUm",
];

const secondRoundMessage =
  "You did a great job! Your design is novel and feasible. Please come up with another idea of sustainable washing machines, potentially with a different focus.";

function ChatbotPage() {
  const filter = require("leo-profanity");

  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [context, setContext] = useState("");
  const [partIndex, setPartIndex] = useState(0);
  const [userInputPhase, setUserInputPhase] = useState("enquiry");
  const [enquiryPhaseStage, setEnquiryPhaseStage] = useState("prompt");
  const [chatHistory, setChatHistory] = useState([]);

  const [vfailCount, setVfailCount] = useState(0);
  const [nfailCount, setNfailCount] = useState(0);
  const [ffailCount, setFfailCount] = useState(0);

  const [endReached, setEndReached] = useState(false);

  const [submitDisable, setSubmitDisable] = useState(false);

  const [rerender, setRerender] = useState(false);

  // const [userInput, setUserInput] = useState("");
  const [isIdle, setIsIdle] = useState(false);
  const [idleCount, setIdleCount] = useState(-1);
  const [inputDetected, setInputDetected] = useState(false);

  const [startTime, setStartTime] = useState(0);
  const [endReachedCount, setendReachedCount] = useState(0);
  const [remaining, setRemaining] = useState(0);

  const messagesEndRef = useRef(null);
  const chatInputForm = useRef(null);
  let listItems = null;

  let idleTimer;

  let idleTimers = [];

  let url = process.env.REACT_APP_API_ENDPOINT;

  const auth = useAuthUser();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  };

  const onIdle = () => {
    console.log("idle");
    //setIsIdle(true);
    console.log(idleCount);
    setIdleCount(idleCount + 1);
    reset();
    // onActive();
    //setIsIdle(false);
  };

  const onActive = () => {
    // setState("Active");
    console.log("active");
    onIdle();
    //setIsIdle(false);
  };

  const onAction = () => {
    console.log("trigerred");
  };

  const { reset, activate, getRemainingTime } = useIdleTimer({
    onIdle,
    onActive,
    onAction,
    events: ["keydown"],
    timeout: 30_000,
    throttle: 500,
  });

  useEffect(() => {
    localStorage.setItem("chatMessages", JSON.stringify(messages));
    localStorage.setItem("chatContext", JSON.stringify(context));
    scrollToBottom();
  }, [messages, context]);

  useEffect(() => {}, [chatHistory]);

  // On message state update, save the chats is the last message is the feedback form
  useEffect(() => {
    reset();
    setRerender(!rerender);
    try {
      let lastMessage = messages[messages.length - 1];
      if (
        lastMessage.content.trim().toLowerCase().includes("http") &&
        lastMessage.sender === "bot"
      ) {
        saveChatHistory();
      }
      scrollToBottom();
    } catch (e) {}
  }, [messages]);

  // On component load, set the intro message, get chats for the user, set the start time and start the timer
  useEffect(() => {
    setPartIndex(0);
    setEnquiryPhaseStage("prompt");
    setUserInputPhase("enquiry");
    setMessages(botIntro);
    getChatHistory();
    setStartTime(Date.now());
    console.log(startTime);

    // // Attach event listeners
    // window.addEventListener("keydown", //handleUserTyping);

    // // Initial start of the idle timer
    // //startIdleTimer();

    // // Clean up event listeners on component unmount
    // return () => {
    //   window.removeEventListener("keydown", //handleUserTyping);
    //   clearTimeout(idleTimer);
    // };

    const interval = setInterval(() => {
      setRemaining(Math.ceil(getRemainingTime() / 1000));
    }, 500);

    return () => {
      clearInterval(interval);
    };
  }, []);

  // Handle the timer and idleCount
  useEffect(() => {
    console.log(isIdle);
    console.log(idleCount);
    if (!inputDetected && !submitDisable) {
      // Removed isIdle === true &&
      if (idleCount == 0) {
        console.log("Idle for 30 seconds");
        let body = {
          sender: "bot",
          content: "Now, tell me your idea of the washing machines.",
        };
        setMessages((prevState) => [...prevState, body]);
      } else if (idleCount == 1) {
        let body = {
          sender: "bot",
          content: `Let me help you with an example to get you started, "The machine is manufactured from parts that generate less electronic waste and are easy to take apart and recycle".`,
        };
        setMessages((prevState) => [...prevState, body]);
      } else if (idleCount == 3) {
        printFeedback(0);
      } else if (idleCount > 3) {
        return;
      }
      // setIdleCount((prevState) => prevState + 1);
      //handleUserTyping();
      console.log(idleCount);
    }
  }, [idleCount]);

  // const //handleUserTyping = () => {
  //   setIsIdle(false);
  //   clearTimeout(idleTimer);
  //   //startIdleTimer();
  //   //console.log("typed", idleTimer);
  // };

  // // Start the idle timer
  // const //startIdleTimer = () => {
  //   // console.log("called", idleTimers);
  //   // idleTimers.forEach((element) => {
  //   //   clearTimeout(element);
  //   // });
  //   // idleTimers = [];

  //   clearTimeout(idleTimer);
  //   idleTimer = setTimeout(() => {
  //     setIsIdle(false);
  //     setIsIdle(true);
  //   }, 30000); // 30 seconds
  //   //idleTimers.push(idleTimer);
  //   //console.log("timers ", idleTimers);
  //   console.log("new ", idleTimer);
  // };

  const checkForProfanity = async (str) => {
    console.log(str);
    let temp = filter.clean(str);
    console.log(temp, temp.includes("*"));
    if (temp.includes("*")) {
      return true;
    }
    return false;
  };

  const formatData = (input) => {
    if (input > 9) {
      return input;
    } else return `0${input}`;
  };

  // Function to convert
  // 24 Hour to 12 Hour clock
  const formatHour = (input) => {
    if (input > 12) {
      return input - 12;
    }
    return input;
  };

  let format12Hour = ({ dd, mm, yyyy, hh, MM, SS }) => {
    return `${mm}/${dd}/${yyyy} ${hh}:${MM}:${SS}`;
  };

  const getChatHistory = async () => {
    let body = {
      email: auth().email,
    };
    let { data } = await axios.post(`${url}/get-chats`, body);

    setChatHistory(data.chats);
    return null;
  };

  // Save the chats to the DB
  const saveChatHistory = async () => {
    console.log("Chat history: ", messages);
    let date = new Date();
    const format = {
      dd: formatData(date.getDate()),
      mm: formatData(date.getMonth() + 1),
      yyyy: date.getFullYear(),
      HH: formatData(date.getHours()),
      hh: formatData(formatHour(date.getHours())),
      MM: formatData(date.getMinutes()),
      SS: formatData(date.getSeconds()),
    };

    let body = {
      email: auth().email,
      timestamp: format12Hour(format),
      chats: messages,
    };
    console.log(body);
    try {
      if (messages.length > 1) {
        let history = await axios.post(`${url}/save-chat`, body);
        if (chatHistory.length == 0) {
          setChatHistory([{ chat: body.chats, timestamp: body.timestamp }]);
        } else {
          setChatHistory((prevState) => [
            ...prevState,
            { chat: body.chats, timestamp: body.timestamp },
          ]);
        }
      }
    } catch (e) {
      console.log("Could not save the chats");
    }
  };

  const clearChat = () => {
    setMessages([]);
    setContext("");
    localStorage.removeItem("chatMessages");
    localStorage.removeItem("chatContext");
    setMessages([botIntro]);
    setUserInputPhase("enquiry");
    setEnquiryPhaseStage("prompt");
    setPartIndex(0);
  };

  const startNewChat = () => {
    clearChat();
    setStartTime(Date.now());
    setIdleCount(-1);
    //handleUserTyping();
    getChatHistory();
    setSubmitDisable(false);
  };

  const openChatHistory = (index) => {
    setSubmitDisable(true);
    setMessages([]);
    // console.log(chatHistory[index].chat);
    setMessages(chatHistory[index].chat);
  };

  const delay = (ms) => {
    return new Promise((resolve) => {
      setTimeout(resolve, ms);
    });
  };

  const printFeedback = async (success) => {
    let timer = (Date.now() - startTime) / 1000;
    await delay(1000);

    console.log(isIdle);

    if (success) {
      if (endReachedCount < 1) {
        let body = {
          sender: "bot",
          content: secondRoundMessage,
        };
        setMessages((prevState) => [...prevState, body]);
        setInputDetected(false);
        //console.log(isIdle);
        setIdleCount(-1);
        //handleUserTyping();
      } else {
        let bodyFeedback = {
          sender: "bot",
          content: feedbackMessage[0],
        };
        let bodySurvey = {
          sender: "bot",
          content: feedbackMessage[1],
        };
        setMessages((prevState) => [...prevState, bodyFeedback, bodySurvey]);
        setSubmitDisable(true);
      }
    } else {
      let bodyFeedback = {
        sender: "bot",
        content: feedbackMessage[0],
      };
      let bodySurvey = {
        sender: "bot",
        content: feedbackMessage[1],
      };
      setMessages((prevState) => [...prevState, bodyFeedback, bodySurvey]);
      setSubmitDisable(true);
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    let tempInput = input;
    if (input.trim().length === 0) {
      setErrorMessage("Please enter your message first");
      return;
    }

    if (tempInput.trim().split(" ").length === 1) {
      tempInput += " ";
      console.log(tempInput);
    }
    setInput("");
    // if (endReached) {
    //   setSubmitDisable(true);
    //   setMessages((prevState) => [
    //     ...prevState,
    //     {
    //       sender: "user",
    //       content: input.trim(),
    //     },
    //   ]);
    //   saveChatHistory();
    //   return;
    // }

    let response;
    let messagedata = {
      sender: "user",
      content: input,
    };

    setMessages((prevState) => [...prevState, messagedata]);
    scrollToBottom();

    //Handle filler words
    if (fillerWords.includes(input.trim().toLowerCase())) {
      setMessages((prevState) => [
        ...prevState,
        {
          sender: "bot",
          content: "Alright",
        },
      ]);
      return;
    }

    if (Object.keys(greetings).includes(tempInput.toLowerCase())) {
      console.log(greetings[tempInput.toLowerCase()]);
      setMessages((prevState) => [
        ...prevState,
        {
          sender: "bot",
          content: greetings[tempInput.toLowerCase()],
        },
      ]);
      return;
    }

    console.log(checkForProfanity(input.trim()));
    let isProfane = await checkForProfanity(input.trim());
    if (isProfane) {
      setMessages((prevState) => [
        ...prevState,
        {
          sender: "bot",
          content: "Please refrain from use any profanities",
        },
      ]);
      return;
    }

    //console.log(input.trim().split(" "));
    if (input.trim().split(" ").length < 15) {
      setMessages((prevState) => [
        ...prevState,
        {
          sender: "bot",
          content: "Please describe your idea with atleast 15 words",
        },
      ]);
      return;
    }

    setIdleCount(-1);
    setInputDetected(true);

    try {
      let { data } = await axios.post(`${url}/chat`, messagedata);
      let validityMessage = "";

      setMessages((prevState) => [
        ...prevState,
        { sender: "bot", content: validityPassMessage },
      ]);

      if (data["valid"]) {
        setVfailCount(0);
      } else {
        if (vfailCount == 2) {
          validityMessage = validityFailMessages[2];
        } else {
          validityMessage = validityFailMessages[vfailCount];
          setVfailCount(vfailCount + 1);
          setNfailCount(0);
          setFfailCount(0);
        }
        let chatbotValidityRes = {
          sender: "bot",
          content: validityMessage,
        };

        setMessages((prevState) => [...prevState, chatbotValidityRes]);
        scrollToBottom();
      }

      if (data["valid"] == false) {
        if (vfailCount == 2) {
          printFeedback(0);
        }
        return;
      }

      await delay(5000);

      // Novelty check block to check novelty and print message
      let noveltyMessage = "";
      if (data["noveltyScore"] > 0.5) {
        noveltyMessage = noveltyPassMessage;
        setNfailCount(0);
      } else {
        if (nfailCount == 2) {
          noveltyMessage = noveltyFailMessages[2];
          setSubmitDisable(true);
        } else {
          noveltyMessage = noveltyFailMessages[nfailCount];
          setNfailCount(nfailCount + 1);
          setFfailCount(0);
        }
      }

      setRerender(!rerender);
      await delay(2000);

      let chatbotNoveltyRes = {
        sender: "bot",
        content: noveltyMessage,
      };

      setMessages((prevState) => [...prevState, chatbotNoveltyRes]);
      scrollToBottom();

      if (data["noveltyScore"] < 0.5) {
        if (nfailCount == 2) {
          printFeedback(0);
        }
        return;
      }

      //Feasibility check block
      let feasibilityMessage = "";

      if (data["feasibilityScore"] > 0.1) {
        feasibilityMessage = feasibilityPassMessage;
        setFfailCount(0);
      } else {
        if (nfailCount == 2) {
          feasibilityMessage = feasibilityFailMessages[2];
          setSubmitDisable(true);
        } else {
          feasibilityMessage = feasibilityFailMessages[ffailCount];
          setFfailCount(ffailCount + 1);
        }
      }

      setendReachedCount(endReachedCount + 1);
      await delay(5000);

      let chatbotFeasibilityRes = {
        sender: "bot",
        content: feasibilityMessage,
      };

      setMessages((prevState) => [...prevState, chatbotFeasibilityRes]);
      setRerender(!rerender);
      scrollToBottom();

      if (data["feasibilityScore"] < 0.1) {
        if (ffailCount == 2) {
          printFeedback(0);
        }
        return;
      } else {
        printFeedback(1);
        return;
      }
    } catch (error) {
      setMessages((prevState) => [...prevState, chatbotFailMessage]);
      scrollToBottom();
    }

    setInput("");
    setErrorMessage("");
    scrollToBottom();
    //handleUserTyping();
  };

  const onEnterPress = (e) => {
    if (e.keyCode == 13 && e.shiftKey == false) {
      e.preventDefault();
      sendMessage(e);
    }
  };

  return (
    <Container fluid className="flex-container">
      <Row className="g-0">
        <Col xs={3} md={2} lg={2} className="sidebar">
          <div className="description-div">
            <p className="description">
              Hey, welcome to our little experiment. Hope you enjoy chatting
              with me today!
            </p>
            {/* <p className="description">{remaining} seconds remaining</p> */}
          </div>

          <div className="bottomBar">
            <ListGroup className="chat-list-group">
              {chatHistory &&
                chatHistory.map((item, index) => (
                  <ListGroup.Item
                    onClick={() => openChatHistory(index)}
                    as="li"
                    className="d-flex justify-content-between align-items-start chat-list-item"
                  >
                    <div className="ms-2 me-auto list-text">
                      <div className="fw-bold">
                        {item.timestamp && item.timestamp}
                      </div>
                      {item.chat[1].content && item.chat[1].content}
                    </div>
                    <Badge bg="primary" pill>
                      {item.chat.length}
                    </Badge>
                  </ListGroup.Item>
                ))}
            </ListGroup>
          </div>
        </Col>

        <Col xs={9} md={10} lg={10} className="main-bar">
          <div className="chat-messages">
            {messages.length > 0 &&
              messages.map((message, index) => (
                <div className="chat-message-div">
                  {/* <p className={`chat-message ${message.sender}`} key={index}>
                    {message.content}
                  </p> */}
                  {message.content.startsWith("https") ||
                  message.content.startsWith("http") ? (
                    <p className={`chat-message ${message.sender}`}>
                      <a
                        href={message.content}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        {message.content}
                      </a>
                    </p>
                  ) : (
                    <p className={`chat-message ${message.sender}`}>
                      {message.content}
                    </p>
                  )}
                </div>
              ))}
            <div className="chat-message-div" ref={messagesEndRef}></div>
          </div>

          <form
            onSubmit={sendMessage}
            className="chat-form"
            // ref={chatInputForm}
          >
            <div className="d-flex justify-content-center mb-4">
              <div className="form-outline me-3">
                <textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  type="text"
                  id="form1"
                  className="form-control chat-input"
                  onKeyDown={onEnterPress}
                  disabled={submitDisable}
                />
              </div>
              <button
                type="submit"
                className="btn btn-primary btn-chat"
                disabled={submitDisable}
              >
                Send
              </button>
              <button
                className="btn btn-secondary btn-chat"
                onClick={startNewChat}
                style={{ marginLeft: 5 }}
              >
                New Chat
              </button>
            </div>
          </form>
        </Col>
      </Row>
    </Container>
  );
}

export default ChatbotPage;
