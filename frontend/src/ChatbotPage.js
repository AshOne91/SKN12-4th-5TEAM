import React, { useState, useRef, useEffect } from "react";
import "./ChatbotPage.css";
import { FaStethoscope, FaHeartbeat } from "react-icons/fa";

// --- Sidebar 컴포넌트 ---
// 역할: 채팅방 목록 표시 및 새 채팅 시작
function Sidebar({ chats, onNewChat, selectedChatId, onSelectChat, isLoading }) {
  return (
    <div className="sidebar">
      <button className="new-chat-btn" onClick={onNewChat}>
        <FaStethoscope style={{ marginRight: 8 }} />
        새 채팅
      </button>
      <div className="chat-list">
        {isLoading && <div className="chat-item">채팅방 로딩 중...</div>}
        {chats.map((chat) => (
          <div
            key={chat.id} // 백엔드 모델(ChatbotRoomInfo)의 'id' 필드 사용
            className={`chat-item${selectedChatId === chat.id ? " selected" : ""}`}
            onClick={() => onSelectChat(chat.id)}
          >
            <FaHeartbeat style={{ marginRight: 6, color: "#3a8dde" }} />
            {chat.title}
          </div>
        ))}
      </div>
    </div>
  );
}

// --- ChatArea 컴포넌트 ---
// 역할: 메시지 표시, 사용자 입력 처리, 봇 응답 대기 UI
function ChatArea({ messages, onSend, isBotTyping, selectedChatId }) {
  const [input, setInput] = useState("");
  const messagesEndRef = useRef(null);

  // 메시지 목록이 변경될 때마다 스크롤을 맨 아래로 이동
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, isBotTyping]);

  const handleSend = () => {
    // 입력값이 있고, 채팅방이 선택된 경우에만 메시지 전송
    if (input.trim() && selectedChatId) {
      onSend(input);
      setInput("");
    }
  };

  return (
    <div className="chat-area">
      <div className="chat-header">무엇을 도와드릴까요?</div>
      <div className="chat-messages">
        {messages.length === 0 && !isBotTyping ? (
          <div className="chat-placeholder">
            <FaStethoscope size={48} color="#3a8dde" />
            <p>왼쪽에서 채팅을 선택하거나 '새 채팅'을 시작하세요.</p>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div
              key={msg.id || `msg-${idx}`} // 안정적인 key 사용
              className={`chat-bubble ${msg.role === "user" ? "user" : "bot"}`} // 백엔드 모델(ChatbotMessageHistoryItem)의 'role' 필드 사용
            >
              {msg.content} {/* 백엔드 모델의 'content' 필드 사용 */}
            </div>
          ))
        )}
        {/* 봇이 응답을 생성 중일 때 '입력 중' 인디케이터 표시 */}
        {isBotTyping && (
          <div className="chat-bubble bot typing">
            <span></span>
            <span></span>
            <span></span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <div className="chat-input-area">
        <input
          type="text"
          placeholder={selectedChatId ? "무엇이든 물어보세요" : "채팅을 선택해주세요"}
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === "Enter" && handleSend()}
          disabled={!selectedChatId || isBotTyping} // 채팅 미선택 또는 봇 응답 중일 때 비활성화
        />
        <button className="send-btn" onClick={handleSend} disabled={!selectedChatId || isBotTyping}>
          전송
        </button>
      </div>
    </div>
  );
}

// --- 메인 ChatbotPage 컴포넌트 ---
// 역할: 전체 상태 관리 및 API 연동
function ChatbotPage() {
  const [chats, setChats] = useState([]); // 채팅방 목록
  const [selectedChatId, setSelectedChatId] = useState(null); // 선택된 채팅방 ID
  const [messages, setMessages] = useState([]); // 현재 채팅방의 메시지 목록
  const [isLoadingRooms, setIsLoadingRooms] = useState(false); // 채팅방 로딩 상태
  const [isLoadingHistory, setIsLoadingHistory] = useState(false); // 대화내역 로딩 상태
  const [isBotTyping, setIsBotTyping] = useState(false); // 봇 응답 대기 상태
  const [error, setError] = useState(null); // 에러 상태

  const API_BASE_URL = "http://localhost:8000/chatbot";
  const SEQUENCE = 0;
  const getAccessToken = () => localStorage.getItem("accessToken") || "";

  // 1. 컴포넌트가 처음 렌더링될 때 채팅방 목록을 가져옵니다.
  useEffect(() => {
    const fetchRooms = async () => {
      setIsLoadingRooms(true);
      setError(null);
      try {
        const res = await fetch(`${API_BASE_URL}/rooms`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            accessToken: getAccessToken(),
            sequence: SEQUENCE
          }),
        });
        if (!res.ok) throw new Error("채팅방 목록을 불러오는 데 실패했습니다.");
        
        const data = await res.json(); // ChatbotRoomsResponse
        // data.rooms는 ChatbotRoomInfo 객체 리스트 (id, title)
        setChats(data.rooms || []);
        
        // 첫 번째 채팅방을 자동으로 선택
        if (data.rooms && data.rooms.length > 0) {
          setSelectedChatId(data.rooms[0].id); // 백엔드 모델의 'id' 필드 사용
        }
      } catch (err) {
        setError(err.message);
        console.error(err);
        setChats([]);
      } finally {
        setIsLoadingRooms(false);
      }
    };
    fetchRooms();
  }, []); // 빈 배열을 전달하여 최초 1회만 실행

  // 2. 선택된 채팅방 ID가 변경될 때마다 해당 방의 대화 내역을 가져옵니다.
  useEffect(() => {
    if (!selectedChatId) {
      setMessages([]);
      return;
    }

    const fetchHistory = async () => {
      setIsLoadingHistory(true);
      setError(null);
      try {
        const res = await fetch(`${API_BASE_URL}/history`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            accessToken: getAccessToken(),
            sequence: SEQUENCE,
            roomId: selectedChatId
          }),
        });
        if (!res.ok) throw new Error("대화 내역을 불러오는 데 실패했습니다.");
        
        const data = await res.json(); // ChatbotHistoryResponse
        // data.history는 ChatbotMessageHistoryItem 객체 리스트 (role, content)
        setMessages(data.history || []);
      } catch (err) {
        setError(err.message);
        console.error(err);
        setMessages([]);
      } finally {
        setIsLoadingHistory(false);
      }
    };
    fetchHistory();
  }, [selectedChatId]); // selectedChatId가 바뀔 때마다 실행

  // 3. '새 채팅' 버튼 클릭 시 새로운 채팅방을 생성합니다.
  const handleNewChat = async () => {
    setError(null);
    try {
      const res = await fetch(`${API_BASE_URL}/room/new`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          accessToken: getAccessToken(),
          sequence: SEQUENCE,
          title: `새 채팅방 ${chats.length + 1}`
        }),
      });
      if (!res.ok) throw new Error("새 채팅방 생성에 실패했습니다.");
      
      const data = await res.json(); // ChatbotRoomNewResponse (roomId 필드 포함)
      
      // API 응답(roomId)을 프론트엔드 상태(id)에 맞게 매핑
      const newRoom = { id: data.roomId, title: `새 채팅 ${chats.length + 1}` };
      
      setChats(prevChats => [newRoom, ...prevChats]);
      setSelectedChatId(data.roomId);
    } catch (err) {
      setError(err.message);
      console.error(err);
    }
  };

  // 4. 메시지를 전송하고 봇의 응답을 받습니다.
  const handleSend = async (messageText) => {
    if (!selectedChatId) return;

    // 사용자 메시지를 UI에 즉시 추가 (role, content 사용)
    const userMessage = { role: "user", content: messageText, id: Date.now() };
    setMessages(prev => [...prev, userMessage]);
    setIsBotTyping(true);
    setError(null);

    try {
      // API 요청 본문은 백엔드 명세(ChatbotMessageRequest)에 맞게 roomId, message 사용
      const res = await fetch(`${API_BASE_URL}/message`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          accessToken: getAccessToken(),
          sequence: SEQUENCE,
          roomId: selectedChatId,
          message: messageText
        }),
      });

      if (!res.ok) throw new Error("메시지 전송에 실패했습니다.");

      const data = await res.json(); // ChatbotMessageResponse (answer 필드 포함)
      
      // 봇의 응답 메시지를 UI에 추가 (role, content 사용)
      const botMessage = { role: "bot", content: data.answer, id: Date.now() + 1 };
      setMessages(prev => [...prev, botMessage]);

    } catch (err) {
      setError(err.message);
      console.error(err);
      const errorMessage = { role: "bot", content: "죄송합니다, 오류가 발생했습니다.", id: Date.now() + 1 };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsBotTyping(false);
    }
  };

  // 에러가 있을 경우 화면에 표시
  if (error) {
    return <div style={{ color: 'red', padding: '2rem' }}>오류: {error}</div>;
  }

  return (
    <div className="chatbot-main">
      <Sidebar
        chats={chats}
        onNewChat={handleNewChat}
        selectedChatId={selectedChatId}
        onSelectChat={setSelectedChatId}
        isLoading={isLoadingRooms}
      />
      <ChatArea
        messages={messages}
        onSend={handleSend}
        isBotTyping={isBotTyping || isLoadingHistory}
        selectedChatId={selectedChatId}
      />
    </div>
  );
}

export default ChatbotPage;
