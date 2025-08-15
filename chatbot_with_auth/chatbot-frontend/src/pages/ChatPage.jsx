// /chatbot-frontend/src/pages/ChatPage.jsx

import { useState, useEffect, useRef } from 'react';
import { useAuth } from '../hooks/useAuth';
import { api, streamMessage } from '../services/api';
import Sidebar from '../components/Sidebar';
import ChatWindow from '../components/ChatWindow';

export default function ChatPage() {
    const { token } = useAuth();
    const [sessions, setSessions] = useState([]);
    const [activeSession, setActiveSession] = useState(null);
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [isHistoryLoading, setIsHistoryLoading] = useState(false);
    const [textQueue, setTextQueue] = useState('');

    const fetchSessions = async () => {
        if (!token) return;
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

    useEffect(() => {
        fetchSessions();
    }, [token]);

    // CHANGE: The state update logic inside the useEffect hook is now fully immutable
    // to prevent the character duplication bug.
    useEffect(() => {
        if (textQueue.length === 0) {
            return;
        }

        const timerId = setTimeout(() => {
            setMessages(prevMessages => {
                // Create a shallow copy of the messages array.
                const updatedMessages = [...prevMessages];
                const lastMessageIndex = updatedMessages.length - 1;

                // Ensure there is a message to update.
                if (lastMessageIndex >= 0) {
                    const lastMessage = updatedMessages[lastMessageIndex];
                    
                    // Check if it's the bot's message placeholder.
                    if (lastMessage && lastMessage.role === 'model') {
                        // Create a brand new message object instead of mutating the old one.
                        const updatedLastMessage = {
                            ...lastMessage,
                            content: lastMessage.content + textQueue[0] // Append the next character.
                        };
                        // Replace the old message with our new, updated message object.
                        updatedMessages[lastMessageIndex] = updatedLastMessage;
                    }
                }
                return updatedMessages;
            });

            // Remove the character we just processed from the queue.
            setTextQueue(prevQueue => prevQueue.substring(1));
        }, 5); // Adjust this value for faster or slower typing speed.

        return () => clearTimeout(timerId);

    }, [textQueue, messages]); // Add 'messages' as a dependency to ensure we always have the latest state.


    const handleSelectSession = async (sessionId) => {
        setIsLoading(true);
        setActiveSession(sessionId);
        try {
            const data = await api.getChatHistory(token, sessionId);
            setMessages(data.messages);
        } catch (error) {
            console.error("Failed to fetch chat history:", error);
            setMessages([]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleNewChat = () => {
        setActiveSession(null);
        setMessages([]);
    };

    const handleSendMessage = async (prompt) => {
        const optimisticUserMessage = { id: `user-${Date.now()}`, role: 'user', content: prompt };
        const botPlaceholder = { id: `model-${Date.now()}`, role: 'model', content: '' };
        
        setMessages(prev => [...prev, optimisticUserMessage, botPlaceholder]);
        setIsLoading(true);

        try {
            await streamMessage(
                token,
                prompt,
                activeSession,
                (chunk) => {
                    setTextQueue(prevQueue => prevQueue + chunk);
                }
            );

        } catch (error) {
            console.error("--- DEBUG: Failed to stream message:", error);
            setMessages(prev => {
                const updated = [...prev];
                const last = updated[updated.length - 1];
                if (last && last.role === 'model') {
                    last.content = 'Error: Could not get a response from the server.';
                }
                return updated;
            });
        } finally {
            setIsLoading(false);
            fetchSessions();
        }
    };

    const handleDeleteSession = async (sessionId) => {
        try {
            await api.deleteChatSession(token, sessionId);
            setSessions(prev => prev.filter(s => s.id !== sessionId));
            if (activeSession === sessionId) {
                handleNewChat();
            }
        } catch (error) {
            console.error("Failed to delete session:", error);
        }
    };

    const handleRenameSession = async (sessionId, newTitle) => {
        try {
            const updatedSession = await api.renameChatSession(token, sessionId, newTitle);
            setSessions(prev => prev.map(s => s.id === sessionId ? updatedSession : s));
        } catch (error) {
            console.error("Failed to rename session:", error);
        }
    };

    return (
        <div className="flex h-screen font-sans">
            <Sidebar
                sessions={sessions}
                onSelectSession={handleSelectSession}
                onNewChat={handleNewChat}
                onDeleteSession={handleDeleteSession}
                onRenameSession={handleRenameSession}
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
