// src/components/ChatWindow.jsx

import { useState, useEffect, useRef } from 'react';
import { Send, MessageCircle } from 'lucide-react';
import ChatMessage from './ChatMessage';

export default function ChatWindow({ messages, onSendMessage, isLoading }) {
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
        <div className="flex-1 flex flex-col bg-hsl(var(--background))">
            <div className="flex-1 p-6 overflow-y-auto">
                {messages.length === 0 && !isLoading && (
                    <div className="flex flex-col items-center justify-center h-full text-hsl(var(--muted-foreground))">
                        <MessageCircle className="w-20 h-20 mb-4 opacity-20" />
                        <h2 className="text-2xl font-semibold">Welcome to the Chatbot</h2>
                        <p className="text-hsl(var(--muted-foreground))">Start a new conversation or select one from your history.</p>
                    </div>
                )}
                {messages.map((msg) => <ChatMessage key={msg.id || Date.now()} message={msg} />)}
                {isLoading && <ChatMessage message={{ role: 'model', content: '...' }} />}
                <div ref={messagesEndRef} />
            </div>
            <div className="p-4 bg-hsl(var(--background))/80 backdrop-blur-sm border-t border-hsl(var(--border))">
                <div className="relative">
                    <textarea
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={(e) => {
                            if (e.key === 'Enter' && !e.shiftKey) {
                                e.preventDefault();
                                handleSend();
                            }
                        }}
                        placeholder="Type your message..."
                        className="w-full pl-4 pr-16 py-3 text-black bg-hsl(var(--input)) border border-transparent rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none transition-all"
                        rows="1"
                        onInput={(e) => {
                            e.target.style.height = 'auto';
                            e.target.style.height = `${e.target.scrollHeight}px`;
                        }}
                    />
                    <button 
                        onClick={handleSend} 
                        className="absolute right-3 top-1/2 -translate-y-1/2 p-2 bg-blue-600 rounded-full hover:bg-blue-700 transition-all disabled:bg-gray-500"
                        disabled={!input.trim()}
                    >
                        <Send className="w-5 h-5 text-white" />
                    </button>
                </div>
            </div>
        </div>
    );
};
