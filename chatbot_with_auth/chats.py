from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session, select
from typing import List, Optional
from pydantic import BaseModel
from limiter import limiter
from database import get_session
from models import User, ChatSession, ChatMessage
from dependencies import get_current_active_user
from chatbot_service import get_chatbot_response
from slowapi import Limiter

CHAT_RATE_LIMIT = "30/minute"
# Define the router
router = APIRouter(
    prefix="/chats",
    tags=["Chats"],
    dependencies=[Depends(get_current_active_user)],
    responses={404: {"description": "Not found"}},
)

# --- Pydantic Models for API Requests and Responses ---

class ChatMessageResponse(BaseModel):
    id: int
    content: str
    role: str

class ChatSessionResponse(BaseModel):
    id: int
    title: str

class ChatHistoryResponse(BaseModel):
    id: int
    title: str
    messages: List[ChatMessageResponse]

class NewChatMessageRequest(BaseModel):
    prompt: str
    session_id: Optional[int] = None


# --- API Endpoints ---

@router.get("/", response_model=List[ChatSessionResponse], summary="Get all chat sessions for the current user")
def get_user_chat_sessions(
    *, 
    session: Session = Depends(get_session), 
    current_user: User = Depends(get_current_active_user)
):
    """
    Fetches a list of all chat session titles and their IDs for the logged-in user,
    which is perfect for populating the sidebar.
    """
    return current_user.sessions

@router.get("/{session_id}", response_model=ChatHistoryResponse, summary="Get the history of a specific chat session")
def get_chat_history(
    *, 
    session_id: int, 
    session: Session = Depends(get_session), 
    current_user: User = Depends(get_current_active_user)
):
    
    """
    Fetches all messages for a given session ID, but only if it belongs to the current user.
    """
    chat_session = session.get(ChatSession, session_id)
    if not chat_session or chat_session.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat session not found")
    return chat_session

@router.post("/", response_model=ChatHistoryResponse, summary="Post a new message")
def post_new_message(
    *,
    limiter: Limiter = Depends(lambda: limiter.limit(CHAT_RATE_LIMIT)),
    request_data: NewChatMessageRequest, # Renamed to avoid conflict
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    """
    This is the core endpoint. It handles:
    1. Creating a new chat session if no session_id is provided.
    2. Adding the user's new message to the database.
    3. Getting a response from the LangChain service.
    4. Saving the bot's response to the database.
    5. Returning the entire updated chat session.
    """
    chat_session = None

    # Case 1: Continue an existing chat session
    if request_data.session_id:
        chat_session = session.get(ChatSession, request_data.session_id)
        # Security check: ensure the session belongs to the current user
        if not chat_session or chat_session.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Chat session not found")
    
    # Case 2: Start a new chat session
    else:
        # Create a title for the session from the first 100 chars of the prompt
        title = request_data.prompt[:100]
        chat_session = ChatSession(title=title, user_id=current_user.id)
        session.add(chat_session)
        session.commit()
        session.refresh(chat_session)

    # Add the user's message to the database
    user_message = ChatMessage(content=request_data.prompt, role="user", session_id=chat_session.id)
    session.add(user_message)
    
    # Get the chatbot's response using the LangChain service
    bot_response_content = get_chatbot_response(request_data.prompt)
    
    # Add the chatbot's message to the database
    bot_message = ChatMessage(content=bot_response_content, role="model", session_id=chat_session.id)
    session.add(bot_message)

    session.commit()
    # Refresh the session to load the new messages before returning
    session.refresh(chat_session)

    return chat_session
