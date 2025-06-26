import React, { useState, useRef, useEffect } from "react";
import "./ChatbotPage.css";
import { FaPlus, FaStethoscope, FaHeartbeat } from "react-icons/fa";

function Sidebar({ chats, onNewChat, onAddChat, selectedChat, onSelectChat }) {
  return (
    <div className="sidebar">
      <button className="new-chat-btn" onClick={onNewChat}>
        <FaStethoscope style={{ marginRight: 8 }} />
        새 채팅
      </button>
      <div className="chat-list">
        {chats.map((chat, idx) => (
          <div
            key={chat.id}
            className={`chat-item${selectedChat === chat.id ? " selected" : ""}`}
            onClick={() => onSelectChat(chat.id)}
          >
            <FaHeartbeat style={{ marginRight: 6, color: "#3a8dde" }} />
            {chat.title}
          </div>
        ))}
      </div>
      <button className="add-chat-btn" onClick={onAddChat}>
        <FaPlus /> 채팅 추가
      </button>
    </div>
  );
}

function ChatArea({ messages, onSend }) {
  const [input, setInput] = useState("");
  const messagesEndRef = useRef(null);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const handleSend = () => {
    if (input.trim()) {
      onSend(input);
      setInput("");
    }
  };

  return (
    <div className="chat-area">
      <div className="chat-header">무엇을 도와드릴까요?</div>
      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="chat-placeholder">
            <FaStethoscope size={48} color="#3a8dde" />
            <p>무엇이든 물어보세요</p>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div
              key={idx}
              className={`chat-bubble ${msg.role === "user" ? "user" : "bot"}`}
            >
              {msg.text}
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>
      <div className="chat-input-area">
        <input
          type="text"
          placeholder="무엇이든 물어보세요"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === "Enter" && handleSend()}
        />
        <button className="send-btn" onClick={handleSend}>
          전송
        </button>
      </div>
    </div>
  );
}

function ChatbotPage() {
  const [chats, setChats] = useState([
    { id: 1, title: "건강 상담" },
    { id: 2, title: "영양 정보" }
  ]);
  const [selectedChat, setSelectedChat] = useState(1);
  const [messages, setMessages] = useState([]);

  const handleNewChat = () => {
    setMessages([]);
    setSelectedChat(null);
  };

  const handleAddChat = () => {
    const newId = chats.length + 1;
    setChats([...chats, { id: newId, title: `새 채팅 ${newId}` }]);
  };

  const handleSelectChat = (id) => {
    setSelectedChat(id);
    setMessages([]); // 임시: 채팅별 메시지 분리 필요시 수정
  };

  const handleSend = async (text) => {
    // 1. 사용자 메시지를 즉시 채팅창에 추가
    const userMessage = { role: "user", text };
    setMessages(prevMessages => [...prevMessages, userMessage]);

    try {
      // 2. 백엔드 API에 질문 전송 (엔드포인트는 예시입니다)
      const res = await fetch("http://127.0.0.1:8000/emergency-support/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: text }),
      });

      if (!res.ok) {
        throw new Error("서버 응답 오류");
      }

      const data = await res.json(); // 백엔드로부터 { "answer": "..." } 형태의 응답을 기대
      const botMessage = { role: "bot", text: data.answer };
      setMessages(prevMessages => [...prevMessages, botMessage]);
    } catch (error) {
      console.error("챗봇 응답을 가져오는 데 실패했습니다:", error);
      const errorMessage = { role: "bot", text: "죄송합니다, 오류가 발생했습니다." };
      setMessages(prevMessages => [...prevMessages, errorMessage]);
    }
  };

  return (
    <div className="chatbot-main">
      <Sidebar
        chats={chats}
        onNewChat={handleNewChat}
        onAddChat={handleAddChat}
        selectedChat={selectedChat}
        onSelectChat={handleSelectChat}
      />
      <ChatArea messages={messages} onSend={handleSend} />
    </div>
  );
}

export default ChatbotPage;
