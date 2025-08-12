import { useState, useEffect, useRef, createContext, useContext } from 'react';
import { Plus, LogOut, Send, Bot, User, MessageCircle } from 'lucide-react';

// --- Configuration ---
// Make sure your FastAPI backend is running on this URL
const API_BASE_URL = 'http://127.0.0.1:8000';

// --- Authentication Context ---
const AuthContext = createContext();

const AuthProvider = ({ children }) => {
    const [token, setToken] = useState(localStorage.getItem('authToken'));

    const login = (newToken) => {
        localStorage.setItem('authToken', newToken);
        setToken(newToken);
    };

    const logout = () => {
        localStorage.removeItem('authToken');
        setToken(null);
    };

    return (
        <AuthContext.Provider value={{ token, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

const useAuth = () => useContext(AuthContext);

// --- API Service ---
const api = {
    async login(username, password) {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        const response = await fetch(`${API_BASE_URL}/auth/token`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData,
        });
        if (!response.ok) throw new Error('Login failed');
        const data = await response.json();
        return data.access_token;
    },
    async getChatSessions(token) {
        const response = await fetch(`${API_BASE_URL}/chats/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('Failed to fetch sessions');
        return response.json();
    },
    async getChatHistory(token, sessionId) {
        const response = await fetch(`${API_BASE_URL}/chats/${sessionId}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('Failed to fetch history');
        return response.json();
    },
    async postMessage(token, prompt, sessionId) {
        const response = await fetch(`${API_BASE_URL}/chats/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt, session_id: sessionId }),
        });
        if (!response.ok) throw new Error('Failed to post message');
        return response.json();
    }
};

// --- Components ---

const LoginPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const { login } = useAuth();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        try {
            const token = await api.login(username, password);
            login(token);
        } catch (err) {
            setError('Incorrect username or password.');
        }
    };

    return (
      <div
  className="flex items-center justify-center h-screen bg-gray-900 text-white bg-cover bg-center"
  style={{ backgroundImage: "url('https://e0.pxfuel.com/wallpapers/630/410/desktop-wallpaper-the-search-nfrealmusic-nf-the-rapper.jpg')" }}
>
            <div className="w-full max-w-md p-8 space-y-8 bg-gray-800 rounded-xl shadow-lg">
                <h2 className="text-3xl font-bold text-center text-white">Chatbot Login</h2>
                <form className="space-y-6" onSubmit={handleSubmit}>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="Username"
                        className="w-full px-4 py-2 text-white bg-gray-700 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                    />
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Password"
                        className="w-full px-4 py-2 text-white bg-gray-700 border border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                    />
                    {error && <p className="text-red-400 text-sm">{error}</p>}
                    <button type="submit" className="w-full px-4 py-2 font-bold text-white bg-blue-600 rounded-md hover:bg-blue-700 transition-colors">
                        Login
                    </button>
                </form>
            </div>
        </div>
    );
};

const Sidebar = ({ sessions, onSelectSession, onNewChat, activeSessionId, isLoading }) => {
    const { logout } = useAuth();
    return (
        <div className="w-64 bg-gray-800 flex flex-col p-4">
            <button onClick={onNewChat} className="flex items-center justify-center w-full px-4 py-2 mb-4 font-semibold text-white bg-blue-600 rounded-md hover:bg-blue-700 transition-colors">
                <Plus className="w-4 h-4 mr-2" /> New Chat
            </button>
            <div className="flex-grow overflow-y-auto">
                <h2 className="text-xs font-bold tracking-wider text-gray-400 uppercase mb-2">History</h2>
                {isLoading ? (
                    <p className="text-gray-400">Loading...</p>
                ) : (
                    sessions.map(session => (
                        <button
                            key={session.id}
                            onClick={() => onSelectSession(session.id)}
                            className={`w-full text-left px-3 py-2 text-sm rounded-md truncate transition-colors ${
                                activeSessionId === session.id ? 'bg-gray-700' : 'hover:bg-gray-700'
                            }`}
                        >
                            {session.title}
                        </button>
                    ))
                )}
            </div>
            <button onClick={logout} className="flex items-center justify-center w-full px-4 py-2 mt-4 text-sm font-semibold text-gray-300 bg-gray-700 rounded-md hover:bg-red-600 hover:text-white transition-colors">
                <LogOut className="w-4 h-4 mr-2" /> Logout
            </button>
        </div>
    );
};

const ChatMessageComponent = ({ message }) => {
    const isUser = message.role === 'user';
    return (
        <div className={`flex items-start gap-3 my-4 ${isUser ? 'justify-end' : ''}`}>
            {!isUser && <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center flex-shrink-0"><Bot className="w-5 h-5"/></div>}
            <div className={`p-3 rounded-lg max-w-lg ${isUser ? 'bg-blue-600' : 'bg-gray-700'}`}>
                <p className="text-sm">{message.content}</p>
            </div>
            {isUser && <div className="w-8 h-8 rounded-full bg-gray-600 flex items-center justify-center flex-shrink-0"><User className="w-5 h-5"/></div>}
        </div>
    );
};

const ChatWindow = ({ messages, onSendMessage, isLoading }) => {
    const [input, setInput] = useState('');
    const messagesEndRef = useRef(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    const handleSend = () => {
        if (input.trim()) {
            onSendMessage(input);
            setInput('');
        }
    };

    return (
        <div className="flex-1 flex flex-col bg-gray-900">
            <div className="flex-1 p-6 overflow-y-auto">
                {messages.length === 0 && !isLoading && (
                    <div className="flex flex-col items-center justify-center h-full text-gray-500">
                        <MessageCircle className="w-16 h-16 mb-4" />
                        <h2 className="text-2xl font-semibold">Chatbot</h2>
                        <p>Start a new conversation or select one from the history.</p>
                    </div>
                )}
                {messages.map((msg, index) => <ChatMessageComponent key={index} message={msg} />)}
                {isLoading && <ChatMessageComponent message={{ role: 'model', content: 'Thinking...' }} />}
                <div ref={messagesEndRef} />
            </div>
            <div className="p-4 bg-gray-800 border-t border-gray-700">
                <div className="relative">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                        placeholder="Type your message..."
                        className="w-full pl-4 pr-12 py-2 text-white bg-gray-700 border border-gray-600 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <button onClick={handleSend} className="absolute right-2 top-1/2 -translate-y-1/2 p-2 bg-blue-600 rounded-full hover:bg-blue-700 transition-colors">
                        <Send className="w-4 h-4 text-white" />
                    </button>
                </div>
            </div>
        </div>
    );
};

const ChatPage = () => {
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


function App() {
    const { token } = useAuth();
    return  <ChatPage />;
}

// This is the main export
export default function WrappedApp() {
  return (
    <AuthProvider>
      <App />
    </AuthProvider>
  );
}
