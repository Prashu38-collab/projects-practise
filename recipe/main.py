import os
import uuid
from datetime import date
from typing import Optional
    
import auth
import database
from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.staticfiles import StaticFiles
from PIL import Image
from pydantic import BaseModel

app = FastAPI()

# Ensure uploads directory exists
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Initialize database
database.init_db()

class UserCreate(BaseModel):
    username: str
    password: str

@app.post("/signup")
def signup(user: UserCreate):
    conn = database.get_db()
    cursor = conn.cursor()
    
    existing = cursor.execute("SELECT * FROM users WHERE username = ?", (user.username,)).fetchone()
    if existing:
        conn.close()
        raise HTTPException(status_code=400, detail="Username already registered")
        
    hashed_password = auth.get_password_hash(user.password)
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user.username, hashed_password))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    
    return {"message": "User created successfully", "id": user_id}

class LoginData(BaseModel):
    username: str
    password: str

@app.post("/api/login")
def api_login(data: LoginData):
    conn = database.get_db()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (data.username,)).fetchone()
    conn.close()
    
    if not user or not auth.verify_password(data.password, user['password']):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
        
    access_token = auth.create_access_token(data={"sub": user['username'], "id": user['id']})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/recipes")
def get_recipes(
    page: int = 1, 
    limit: int = 10, 
    keyword: Optional[str] = None, 
    chef: Optional[str] = None, 
    labels: Optional[str] = None, 
    publication_date: Optional[str] = None
):
    conn = database.get_db()
    offset = (page - 1) * limit
    
    query = "SELECT recipes.*, users.username AS chef_name FROM recipes JOIN users ON recipes.chef_id = users.id WHERE 1=1"
    params = []
    
    if keyword:
        query += " AND (recipes.title LIKE ? OR recipes.keywords LIKE ?)"
        params.extend([f"%{keyword}%", f"%{keyword}%"])
    if chef:
        query += " AND users.username = ?"
        params.append(chef)
    if labels:
        query += " AND recipes.labels LIKE ?"
        params.append(f"%{labels}%")
    if publication_date:
        query += " AND recipes.publication_date = ?"
        params.append(publication_date)
        
    count_query = query.replace("SELECT recipes.*, users.username AS chef_name", "SELECT COUNT(*) as count")
    
    query += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    count_row = conn.execute(count_query, params[:-2]).fetchone()
    total = count_row['count']
    
    rows = conn.execute(query, params).fetchall()
    conn.close()
    
    return {
        "data": [dict(row) for row in rows],
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": (total + limit - 1) // limit
    }

@app.post("/recipes")
def create_recipe(
    title: str = Form(...),
    description: str = Form(...),
    keywords: str = Form(""),
    labels: str = Form(""),
    image: UploadFile = File(None),
    current_user: dict = Depends(auth.get_current_user)
):
    image_url = None
    if image:
        filename = f"{uuid.uuid4().hex}.jpg"
        filepath = os.path.join(UPLOAD_DIR, filename)
        
        # Process image with Pillow
        try:
            with Image.open(image.file) as img:
                img = img.convert("RGB")
                img.thumbnail((800, 600))
                img.save(filepath, "JPEG", quality=80)
            image_url = f"/uploads/{filename}"
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error processing image")
            
    conn = database.get_db()
    cursor = conn.cursor()
    pub_date = date.today().isoformat()
    
    cursor.execute(
        "INSERT INTO recipes (title, description, keywords, publication_date, chef_id, labels, image_url) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (title, description, keywords, pub_date, current_user['id'], labels, image_url)
    )
    conn.commit()
    recipe_id = cursor.lastrowid
    conn.close()
    
    return {"message": "Recipe created", "id": recipe_id, "image_url": image_url}
