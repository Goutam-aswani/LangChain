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
from fastapi.responses import StreamingResponse

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

class RenameChatRequest(BaseModel):
    new_title: str

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


async def stream_and_save_response(prompt: str, chat_session: ChatSession, db: Session):
    """
    Streams the chatbot response to the client and saves the full message to the DB upon completion.
    """
    # DEBUG: Log the start of the streaming process for a specific session.
    print(f"--- DEBUG: Starting stream for session {chat_session.id} ---")
    
    # 1. Get the streaming generator from the chatbot service.
    response_generator = get_chatbot_response(prompt)
    
    full_bot_response = ""
    
    # 2. Stream chunks to the client and simultaneously build the full response string.
    for chunk in response_generator:
        full_bot_response += chunk
        # DEBUG: Log the specific chunk being sent to the client.
        print(f"--- DEBUG: CLIENT CHUNK: {chunk}")
        yield chunk
        
    # DEBUG: Log when streaming to the client has finished and show the full response.
    print(f"--- DEBUG: Finished streaming to client for session {chat_session.id} ---")
    print(f"--- DEBUG: Full bot response to be saved: '{full_bot_response}'")
    
    # 3. Once streaming is complete, save the single, full bot message to the database.
    bot_message_to_save = ChatMessage(
        content=full_bot_response, 
        role="model", 
        session_id=chat_session.id
    )
    db.add(bot_message_to_save)
    db.commit()
    
    # DEBUG: Confirm that the bot's message has been saved to the database.
    print(f"--- DEBUG: Saved full bot response to DB for session {chat_session.id} ---")


@router.post("/", summary="Post a new message and get a streaming response")
def post_new_message(
    *,
    limiter: Limiter = Depends(lambda: limiter.limit(CHAT_RATE_LIMIT)),
    request_data: NewChatMessageRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    """
    This is the core endpoint. It handles:
    1. Creating or finding the chat session.
    2. Saving the user's message.
    3. Returning a StreamingResponse from the chatbot.
    4. The helper function then saves the bot's full response after the stream ends.
    """
    chat_session = None

    # Case 1: Continue an existing chat session
    if request_data.session_id:
        chat_session = session.get(ChatSession, request_data.session_id)
        if not chat_session or chat_session.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Chat session not found")
    
    # Case 2: Start a new chat session
    else:
        title = request_data.prompt[:100]
        chat_session = ChatSession(title=title, user_id=current_user.id)
        session.add(chat_session)
        session.commit()
        session.refresh(chat_session)

    # Add the user's message to the database
    user_message = ChatMessage(content=request_data.prompt, role="user", session_id=chat_session.id)
    session.add(user_message)
    session.commit()
    # DEBUG: Confirm user message was saved.
    print(f"--- DEBUG: User message '{request_data.prompt}' saved for session {chat_session.id}")
    
    # CHANGE: Return a StreamingResponse.
    # This takes our async generator and streams its yielded chunks to the client.
    # The media_type "text/plain" is simple and effective for streaming raw text.
    return StreamingResponse(
        stream_and_save_response(request_data.prompt, chat_session, session),
        media_type="text/plain; charset=utf-8"
    )

# @router.post("/", response_model=ChatHistoryResponse, summary="Post a new message")
# def post_new_message(
#     *,
#     limiter: Limiter = Depends(lambda: limiter.limit(CHAT_RATE_LIMIT)),
#     request_data: NewChatMessageRequest, # Renamed to avoid conflict
#     session: Session = Depends(get_session),
#     current_user: User = Depends(get_current_active_user),
# ):
#     """
#     This is the core endpoint. It handles:
#     1. Creating a new chat session if no session_id is provided.
#     2. Adding the user's new message to the database.
#     3. Getting a response from the LangChain service.
#     4. Saving the bot's response to the database.
#     5. Returning the entire updated chat session.
#     """
#     chat_session = None

#     # Case 1: Continue an existing chat session
#     if request_data.session_id:
#         chat_session = session.get(ChatSession, request_data.session_id)
#         # Security check: ensure the session belongs to the current user
#         if not chat_session or chat_session.user_id != current_user.id:
#             raise HTTPException(status_code=404, detail="Chat session not found")
    
#     # Case 2: Start a new chat session
#     else:
#         # Create a title for the session from the first 100 chars of the prompt
#         title = request_data.prompt[:100]
#         chat_session = ChatSession(title=title, user_id=current_user.id)
#         session.add(chat_session)
#         session.commit()
#         session.refresh(chat_session)

#     # Add the user's message to the database
#     user_message = ChatMessage(content=request_data.prompt, role="user", session_id=chat_session.id)
#     session.add(user_message)
    
#     # Get the chatbot's response using the LangChain service
#     bot_response_content = get_chatbot_response(request_data.prompt)
    
#     # Add the chatbot's message to the database
#     bot_message = ChatMessage(content=bot_response_content, role="model", session_id=chat_session.id)
#     session.add(bot_message)

#     session.commit()
#     # Refresh the session to load the new messages before returning
#     session.refresh(chat_session)

#     return chat_session

@router.put("/{session_id}", response_model=ChatSessionResponse, summary="Rename a chat session")
def rename_chat_session(
    session_id: int,
    request_data: RenameChatRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    chat_session = session.get(ChatSession, session_id)
    
    if not chat_session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat session not found")
    if chat_session.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to rename this chat session")
        
    chat_session.title = request_data.new_title
    session.add(chat_session)
    session.commit()
    session.refresh(chat_session)
    
    return chat_session

@router.delete("/{session_id}", status_code=status.HTTP_200_OK, summary="Delete a chat session")
def delete_chat_session(
    *,
    session_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Deletes a chat session and all its associated messages,
    but only if it belongs to the current user.
    """
    chat_session = session.get(ChatSession, session_id)
    
    # Security check: Ensure the session exists and belongs to the current user
    if not chat_session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat session not found")
    if chat_session.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this chat session")
        
    # SQLModel will handle cascading deletes for the messages automatically
    # because of the relationship we defined in models.py
    session.delete(chat_session)
    session.commit()
    
    return {"message": "Chat session deleted successfully"}
