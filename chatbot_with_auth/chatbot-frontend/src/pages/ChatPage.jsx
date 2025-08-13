// src/pages/ChatPage.jsx

import { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth'; 
import { api } from '../services/api';
import Sidebar from '../components/Sidebar';
import ChatWindow from '../components/ChatWindow';

export default function ChatPage() {
    const { token } = useAuth();
    const [sessions, setSessions] = useState([]);
    const [activeSession, setActiveSession] = useState(null);
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [isHistoryLoading, setIsHistoryLoading] = useState(false);

    useEffect(() => {
        if (token) {
            const fetchSessions = async () => {
                setIsHistoryLoading(true);
                try {
                    const data = await api.getChatSessions(token);
                    setSessions(data);
                } catch (error) {
                    console.error("Failed to fetch sessions:", error);
                } finally {
                    setIsHistoryLoading(false);
                }
            };
            fetchSessions();
        }
    }, [token]);

    const handleSelectSession = async (sessionId) => {
        setIsLoading(true);
        setActiveSession(sessionId);
        try {
            const data = await api.getChatHistory(token, sessionId);
            setMessages(data.messages);
        } catch (error) {
            console.error("Failed to fetch chat history:", error);
        } finally {
            setIsLoading(false);
        }
    };
    
    const handleNewChat = () => {
        setActiveSession(null);
        setMessages([]);
    };

    const handleSendMessage = async (prompt) => {
        const optimisticMessage = { id: Date.now(), role: 'user', content: prompt };
        setMessages(prev => [...prev, optimisticMessage]);
        setIsLoading(true);

        try {
            const data = await api.postMessage(token, prompt, activeSession);
            setMessages(data.messages);
            setActiveSession(data.id);
            if (!sessions.some(s => s.id === data.id)) {
                 const newSession = { id: data.id, title: data.title };
                 setSessions(prev => [newSession, ...prev]);
            }
        } catch (error) {
            console.error("Failed to send message:", error);
            setMessages(prev => [...prev, { id: Date.now(), role: 'model', content: 'Error: Could not get a response.' }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex h-screen font-sans">
            <Sidebar
                sessions={sessions}
                onSelectSession={handleSelectSession}
                onNewChat={handleNewChat}
                activeSessionId={activeSession}
                isLoading={isHistoryLoading}
            />
            <ChatWindow
                messages={messages}
                onSendMessage={handleSendMessage}
                isLoading={isLoading}
            />
        </div>
    );
};
