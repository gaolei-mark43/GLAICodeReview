from pydantic import BaseModel
from typing import List, Optional

class FileContent(BaseModel):
    path: str
    content: str
    language: Optional[str] = None  # 可选的语言标识，如 'c', 'python' 等

class ReviewRequest(BaseModel):
    client_type: str  # 'vscode' 或 'gerrit'
    review_mode: str  # 'file', 'commit', 'snippet'
    files: Optional[List[FileContent]] = None
    diff: Optional[str] = None
    code_snippet: Optional[str] = None
    model_type: str  # 'qwen2.5-coder-14b-instruct' 或 'qwen2.5-coder-32b-instruct'
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str
    nonce: str 