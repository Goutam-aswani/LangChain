// /chatbot-frontend/src/pages/ChatPage.jsx

import { useState, useEffect, useRef } from 'react';
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
    
    // Using a ref to hold the interval ID to ensure we can clear it reliably.
    const streamIntervalRef = useRef(null);

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
        // Clear any ongoing text streaming when switching sessions
        if (streamIntervalRef.current) {
            clearInterval(streamIntervalRef.current);
        }
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
        // Clear any ongoing text streaming when starting a new chat
        if (streamIntervalRef.current) {
            clearInterval(streamIntervalRef.current);
        }
        setActiveSession(null);
        setMessages([]);
    };

    const handleSendMessage = async (prompt) => {
        console.log("--- Sending message ---");
        // Clear any previous streaming interval that might still be running
        if (streamIntervalRef.current) {
            clearInterval(streamIntervalRef.current);
        }

        const optimisticUserMessage = { id: `user-${Date.now()}`, role: 'user', content: prompt };
        setMessages(prev => [...prev, optimisticUserMessage]);
        setIsLoading(true);
        console.log("Set loading to true. Showing 'Thinking...'");

        try {
            const data = await api.postMessage(token, prompt, activeSession);
            console.log("Received full response from API:", data);

            const serverMessages = data.messages;
            const fullBotText = serverMessages[serverMessages.length - 1].content;
            console.log("Extracted full bot text:", fullBotText);

            // Set up the initial state for the bot's message (empty content)
            const initialMessages = [...serverMessages];
            initialMessages[initialMessages.length - 1].content = '';
            setMessages(initialMessages);
            
            setIsLoading(false);
            console.log("Set loading to false. Starting simulated stream.");

            let index = 0;
            streamIntervalRef.current = setInterval(() => {
                if (index < fullBotText.length) {
                    // Use functional update to ensure we're always working with the latest state
                    setMessages(prevMessages => {
                        // Create a deep copy to avoid mutation issues
                        const newMessages = JSON.parse(JSON.stringify(prevMessages));
                        const lastMessage = newMessages[newMessages.length - 1];
                        lastMessage.content += fullBotText[index];
                        // console.log(`Streaming char ${index}:`, lastMessage.content); // This logs too much, uncomment if needed
                        return newMessages;
                    });
                    index++;
                } else {
                    console.log("--- Stream finished ---");
                    clearInterval(streamIntervalRef.current);
                    // After streaming, update the session list if a new one was created
                    if (!sessions.some(s => s.id === data.id)) {
                        const newSession = { id: data.id, title: data.title };
                        setSessions(prev => [newSession, ...prev]);
                    }
                }
            }, 30); // Slower interval for better stability and visibility

            setActiveSession(data.id);

        } catch (error) {
            console.error("Failed to send message:", error);
            setIsLoading(false);
            setMessages(prev => [...prev, { id: `error-${Date.now()}`, role: 'model', content: 'Error: Could not get a response.' }]);
        }
    };
    const handleDeleteSession = async (sessionId) => {
        try {
            await api.deleteChatSession(token, sessionId);
            // Remove the session from the local state
            setSessions(prev => prev.filter(s => s.id !== sessionId));
            // If the deleted session was the active one, clear the chat window
            if (activeSession === sessionId) {
                handleNewChat();
            }
        } catch (error) {
            console.error("Failed to delete session:", error);
            // Optionally, show an error message to the user
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




{/*### **Explanation of Changes and Debugging:**

1.  **Using `useRef` for the Interval**:
    * I've added `const streamIntervalRef = useRef(null);` to safely store the ID of our `setInterval`.
    * This ensures that if you send a new message while the old one is still "typing," or if you switch chats, we can reliably clear the old interval (`clearInterval(streamIntervalRef.current);`) and prevent multiple loops from trying to update the state at once.

2.  **Deep Copy of State**:
    * Inside the `setInterval`, I'm now using `JSON.parse(JSON.stringify(prevMessages));`. This creates a completely new copy of the messages array. This is a robust way to prevent accidentally modifying the previous state, which can sometimes cause weird rendering behavior in React.

3.  **Slower Interval**:
    * I've changed the interval speed from `20` to `30` milliseconds. This slightly slower speed can sometimes help prevent state update batching issues and makes the effect easier to observe.

4.  **Console Logs**:
    * **`--- Sending message ---`**: Confirms that `handleSendMessage` has started.
    * **`Set loading to true...`**: Tells you when the "Thinking..." message should appear.
    * **`Received full response from API...`**: This is a crucial one. It will show you the exact data that the backend sent back.
    * **`Extracted full bot text...`**: This confirms that we've correctly isolated the response string we need to stream.
    * **`--- Stream finished ---`**: Confirms that the `setInterval` loop has completed successfully.

Please update your `/chatbot-frontend/src/pages/ChatPage.jsx` file with this code. Then, open your browser's developer console and test it out. The log messages should give us a clear picture of what's happeni */}
