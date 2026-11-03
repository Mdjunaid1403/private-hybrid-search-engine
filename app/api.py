import os

from dotenv import load_dotenv
load_dotenv()

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException,
    Depends,
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware

from app.indexer import build_index
from app.local_search import search_documents
from app.database import (
    get_documents,
    get_document,
    insert_document,
    get_documents_for_search,
    update_document,
    delete_document,
    create_user,
    get_user_by_email,
    get_user_by_id,
    create_password_reset_table,
    save_password_reset_token,
    get_valid_password_reset_token,
    mark_password_reset_token_used,
    update_user_password,
    reset_user_password_transactionally
)

from app.document_parser import extract_text
from app.embeddings import create_chunks, generate_embedding
from app.vector_store import store_chunk
from semantic_search import semantic_search
from hybrid_search import hybrid_search
from app.search import search_web
from combined_search import combined_search

from pydantic import BaseModel
from app.password_utils import (
    hash_password,
    verify_password
)
from app.jwt_utils import (
    create_access_token,
    verify_access_token,
)

import secrets
import hashlib
import resend
from datetime import datetime, timedelta

class RegisterRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


app = FastAPI()

create_password_reset_table()

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    user_id = verify_access_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token."
        )

    return user_id


app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL")],
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest):
    generic_message = (
        "If an account exists with this email, "
        "password recovery instructions will be provided."
    )

    existing_user = get_user_by_email(request.email)

    if existing_user is None:
        return {"message": generic_message}

    reset_token = secrets.token_urlsafe(32)

    token_hash = hashlib.sha256(
        reset_token.encode("utf-8")
    ).hexdigest()

    save_password_reset_token(
    existing_user[0],
    token_hash,
    None
)

    frontend_url = os.getenv(
        "FRONTEND_URL",
        "http://localhost:5173"
    ).rstrip("/")

    reset_link = (
        f"{frontend_url}/reset-password?token={reset_token}"
    )

    resend.api_key = os.getenv("RESEND_API_KEY")

    sender_email = os.getenv(
        "RESEND_FROM_EMAIL",
        "onboarding@resend.dev"
    )

    try:
        resend.Emails.send({
            "from": sender_email,
            "to": [request.email],
            "subject": "Reset your password",
            "html": f"""
                <p>We received a request to reset your password.</p>
                <p>
                    <a href="{reset_link}">
                        Reset your password
                    </a>
                </p>
                <p>
                    If you did not request this, you can ignore this email.
                </p>
                <p>This link can only be used once.</p>
            """,
        })
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to send password-reset email. Please try again later."
        )

    return {"message": generic_message}

@app.post("/reset-password")
def reset_password(request: ResetPasswordRequest):
    if len(request.new_password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters long."
        )

    token_hash = hashlib.sha256(
        request.token.encode("utf-8")
    ).hexdigest()

    reset_record = get_valid_password_reset_token(
        token_hash
    )

    if reset_record is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired password-reset link."
        )

    token_id = reset_record[0]
    user_id = reset_record[1]

    new_password_hash = hash_password(
        request.new_password
    )

    success = reset_user_password_transactionally(
        token_id,
        user_id,
        new_password_hash
    )

    if not success:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired password-reset link."
        )

    return {
        "message": "Password has been reset successfully."
    }

@app.post("/register")
def register_user(user: RegisterRequest):

    password_hash = hash_password(
        user.password
    )

    user_id = create_user(
        user.email,
        password_hash
    )

    if user_id == "duplicate":
        raise HTTPException(
            status_code=409,
            detail="An account with this email already exists."
        )

    return {
        "message": "User registered successfully.",
        "user": {
            "id": user_id,
            "email": user.email
        }
    }

@app.post("/login")
def login_user(user: LoginRequest):

    existing_user = get_user_by_email(
        user.email
    )

    if existing_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    password_is_valid = verify_password(
        user.password,
        existing_user[2]
    )

    if not password_is_valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    access_token = create_access_token(
        existing_user[0]
    )

    return {
        "message": "Login successful.",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": existing_user[0],
            "email": existing_user[1]
        }
    }

@app.get("/me")
def get_current_user_info(
    current_user: int = Depends(get_current_user)
):
    user = get_user_by_id(current_user)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    return {
        "user": {
            "id": user[0],
            "email": user[1]
        }
    }

@app.get("/")
def home():
    return {
        "message": "Private Search Engine API is running"
    }

@app.get("/search")
def search(
    query: str,
    current_user: int = Depends(get_current_user)
):
    documents = get_documents_for_search(current_user)

    index = build_index(documents)

    results = search_documents(index, query)

    formatted_results = []

    document_map = {
        document["filename"]: document
        for document in documents
    }

    for filename, score in results:
        document = document_map[filename]

        preview = " ".join(
            document["content"].split()
        )[:100]

        formatted_results.append({
            "filename": filename,
            "score": score,
            "preview": preview
        })

    return {
        "query": query,
        "results": formatted_results
    }

@app.get("/semantic-search")
def semantic_search_endpoint(
    query: str,
    current_user: int = Depends(get_current_user)
):
    results = semantic_search(query, current_user)

    formatted_results = []

    for result in results:
        formatted_results.append({
            "chunk_id": result[0],
            "document_id": result[1],
            "filename": result[2],
            "chunk_text": result[3],
            "distance": result[4]
    })

    return {
        "query": query,
        "results": formatted_results
    }

@app.get("/hybrid-search")
def hybrid_search_endpoint(
    query: str,
    current_user: int = Depends(get_current_user)
):
    results = hybrid_search(query, current_user)

    return {
        "query": query,
        "results": results
    }

@app.get("/web-search")
def web_search_endpoint(
    query: str,
    current_user: int = Depends(get_current_user)
):
    results = search_web(query)

    return {
        "query": query,
        "results": results
    }

@app.get("/combined-search")
def combined_search_endpoint(
    query: str,
    limit: int = 5,
    current_user: int = Depends(get_current_user)
):
    results = combined_search(
        query,
        current_user,
        private_limit=limit,
        web_limit=limit
    )

    return results

@app.get("/documents")
def documents(
    current_user: int = Depends(get_current_user)
):
    rows = get_documents(current_user)

    formatted_documents = []

    for row in rows:
        formatted_documents.append({
            "id": row[0],
            "filename": row[1],
            # "content": row[2]
        })

    return {
        "documents": formatted_documents
    }

@app.get("/documents/{document_id}")
def get_document_endpoint(
    document_id: int,
    current_user: int = Depends(get_current_user)
):
    row = get_document(document_id, current_user)

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    return {
        "id": row[0],
        "filename": row[1],
        "content": row[2]
    }

@app.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    current_user: int = Depends(get_current_user)
):

    # if not file.filename.lower().endswith(".txt"):
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Only .txt files are allowed."
    #     )

    content = await file.read()

    if not content.strip():
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty."
        )

    try:
        text = extract_text(
            content,
            file.filename
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    document_id = insert_document(
        file.filename,
        text,
        current_user
    )

    if document_id is None:
        raise HTTPException(
            status_code=409,
            detail="A document with this filename already exists."
        )

    chunks = create_chunks(text)

    embeddings = [
        generate_embedding(chunk)
        for chunk in chunks
    ]

    for chunk, embedding in zip(chunks, embeddings):
        store_chunk(
            document_id,
            chunk,
            embedding
        )

    return {
        "message": "Document uploaded successfully.",
        "id": document_id,
        "filename": file.filename
    }


@app.put("/documents/{document_id}")
async def update_document_endpoint(
    document_id: int,
    file: UploadFile = File(...),
    current_user: int = Depends(get_current_user)
):
    if not file.filename.lower().endswith(".txt"):
        raise HTTPException(
            status_code=400,
            detail="Only .txt files are allowed."
        )

    content = await file.read()

    if not content.strip():
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty."
        )

    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file must be valid UTF-8 text."
        )

    updated_id = update_document(
        document_id,
        file.filename,
        text,
        current_user
    )

    if updated_id == "duplicate":
        raise HTTPException(
            status_code=409,
            detail="A document with this filename already exists."
        )

    if updated_id is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    return {
        "message": "Document updated successfully.",
        "id": updated_id,
        "filename": file.filename
    }


@app.delete("/documents/{document_id}")
async def delete_document_endpoint(
    document_id: int,
    current_user: int = Depends(get_current_user)
):
    deleted_id = delete_document(document_id, current_user)

    if deleted_id is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    return {
        "message": "Document deleted successfully.",
        "id": deleted_id
    }