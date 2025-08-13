// src/components/Sidebar.jsx

import { Plus, LogOut, MessageSquare } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';

export default function Sidebar({ sessions, onSelectSession, onNewChat, activeSessionId, isLoading }) {
    const { logout } = useAuth();
    
    return (
        <div className="w-64 bg-hsl(var(--secondary)) flex flex-col p-3">
            <button 
                onClick={onNewChat} 
                className="flex items-center justify-center w-full px-4 py-2 mb-4 font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-all transform hover:scale-105"
            >
                <Plus className="w-4 h-4 mr-2" /> New Chat
            </button>
            <div className="flex-grow overflow-y-auto -mr-2 pr-2">
                <h2 className="text-xs font-bold tracking-wider text-hsl(var(--muted-foreground)) uppercase mb-2 px-2">History</h2>
                {isLoading ? (
                    <p className="text-hsl(var(--muted-foreground)) px-2">Loading...</p>
                ) : (
                    sessions.map(session => (
                        <button
                            key={session.id}
                            onClick={() => onSelectSession(session.id)}
                            className={`flex items-center w-full text-left px-3 py-2 text-sm rounded-lg truncate transition-colors ${
                                activeSessionId === session.id 
                                ? 'bg-blue-600/30 text-white' 
                                : 'text-hsl(var(--muted-foreground)) hover:bg-hsl(var(--accent))'
                            }`}
                        >
                            <MessageSquare className="w-4 h-4 mr-3 flex-shrink-0" />
                            <span className="truncate">{session.title}</span>
                        </button>
                    ))
                )}
            </div>
            <button 
                onClick={logout} 
                className="flex items-center justify-center w-full px-4 py-2 mt-4 text-sm font-semibold text-hsl(var(--muted-foreground)) bg-hsl(var(--secondary)) rounded-lg hover:bg-red-600 hover:text-white transition-colors"
            >
                <LogOut className="w-4 h-4 mr-2" /> Logout
            </button>
        </div>
    );
};
