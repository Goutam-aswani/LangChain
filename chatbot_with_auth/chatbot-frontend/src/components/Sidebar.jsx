// /chatbot-frontend/src/components/Sidebar.jsx

// *** FIX: Import useState, useEffect, and useRef from React ***
import { useState, useEffect, useRef } from 'react';
import { Plus, LogOut, MessageSquare, Trash2, MoreHorizontal, Pencil, Check, X } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';

const SessionItem = ({ session, onSelect, onDelete, onRename, activeSessionId }) => {
    const [menuOpen, setMenuOpen] = useState(false);
    const [isRenaming, setIsRenaming] = useState(false);
    const [title, setTitle] = useState(session.title);
    const inputRef = useRef(null);
    
    useEffect(() => {
        if (isRenaming) {
            inputRef.current?.focus();
            inputRef.current?.select();
        }
    }, [isRenaming]);

    const handleDeleteClick = (e) => {
        e.stopPropagation();
        setMenuOpen(false);
        onDelete(session.id);
    };
    
    const handleRenameClick = (e) => {
        e.stopPropagation();
        setMenuOpen(false);
        setIsRenaming(true);
    };

    const handleSaveRename = (e) => {
        e.stopPropagation();
        if (title.trim()) {
            onRename(session.id, title.trim());
            setIsRenaming(false);
        }
    };
    
    const handleCancelRename = (e) => {
        e.stopPropagation();
        setTitle(session.title); // Reset to original title
        setIsRenaming(false);
    };
    
    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            handleSaveRename(e);
        } else if (e.key === 'Escape') {
            handleCancelRename(e);
        }
    };
    
    const handleMenuToggle = (e) => {
        e.stopPropagation();
        setMenuOpen(prev => !prev);
    };
    
    
    return (
        <div className="relative group bg-zinc-900 hover:bg-slate-700 rounded-xl shadow-lg">
            {isRenaming ? (
                <div className="flex items-center w-full bg-hsl(var(--accent)) rounded-lg">
                    
                    <input
                        ref={inputRef}
                        type="text"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        onKeyDown={handleKeyDown}
                        className="flex-grow bg-transparent px-3 py-2 text-sm text-white outline-none"
                        />
                    <button onClick={handleSaveRename} className="p-2 text-green-400 hover:text-white"><Check className="w-4 h-4" /></button>
                    <button onClick={handleCancelRename} className="p-2 text-red-400 hover:text-white"><X className="w-4 h-4" /></button>
                </div>
            ) : (
                <>
                    <button
                        onClick={() => onSelect(session.id)}
                        className={`flex items-center w-full text-left pl-3 pr-10 py-2 text-sm rounded-lg truncate transition-colors ${
                            activeSessionId === session.id 
                            ? 'bg-blue-600/30 text-white' 
                            : 'text-hsl(var(--muted-foreground)) hover:bg-hsl(var(--accent))'
                        }`}
                        >
                        <MessageSquare className="w-4 h-4 mr-3 flex-shrink-0" />
                        <span className="truncate">{session.title}</span>
                    </button>
                    <button
    onClick={handleMenuToggle}
    className="absolute right-2 top-1/2 -translate-y-1/2 p-1 text-gray-500 rounded-md 
    bg-transparent 
    hidden 
    group-hover:block 
    hover:bg-blue-500 
    hover:text-white"
    title="More options"
>
    <MoreHorizontal className="w-4 h-4" />
</button>

                    {menuOpen && (
                        <div className="absolute z-10 right-0 mt-1 w-32 bg-stone-900 border border-hsl(var(--border)) rounded-md shadow-lg">
                            <button onClick={handleRenameClick} className="flex items-center w-full px-3 py-2 text-sm text-left text-hsl(var(--muted-foreground)) hover:bg-slate-700">
                                <Pencil className="w-4 h-4 mr-2" /> Rename
                            </button>
                            <button onClick={handleDeleteClick} className="flex items-center w-full px-3 py-2 text-sm text-left text-red-500 hover:bg-red-600/20">
                                <Trash2 className="w-4 h-4 mr-2" /> Delete
                            </button>
                        </div>
                    )}
                </>
            )}
        </div>
    );
};


export default function Sidebar({ sessions, onSelectSession, onNewChat, onDeleteSession, onRenameSession, activeSessionId, isLoading }) {
    const { logout } = useAuth();
    const [hide, setHide] = useState(false);
    {hide && (
        <button onClick={() => setHide(!hide)} className="mb-4 text-sm text-hsl(var(--muted-foreground)) hover:text-white">show</button>
    )}
    return (
        <div className={`w-64 bg-zinc-900 flex flex-col p-3 ${hide ? 'hidden' : 'block'}`}>
            <button onClick={() => setHide(!hide)} className="mb-4 text-sm text-hsl(var(--muted-foreground)) hover:text-white">hide
            </button>

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
                        <SessionItem
                            key={session.id}
                            session={session}
                            onSelect={onSelectSession}
                            onDelete={onDeleteSession}
                            onRename={onRenameSession}
                            activeSessionId={activeSessionId}
                        />
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
