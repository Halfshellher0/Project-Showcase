from typing import List
import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm
import services as _services
import schemas as _schemas
from fastapi.middleware.cors import CORSMiddleware

app = _fastapi.FastAPI()

origins = [
    "https://localhost:3000",
    "https://ocalhost:8080",
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/users")
async def create_user(
    user: _schemas.UserCreate,
    admin: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    db_user = await _services.get_user_by_username(user.username, db)
    if db_user:
        raise _fastapi.HTTPException(status_code=400, detail="Username is already in use.")
    
    return await _services.create_user(user, db)

@app.post("/api/token")
async def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    user = await _services.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials")

    return await _services.create_token(user)

@app.get("/api/users/me", response_model=_schemas.User)
async def get_user(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return user

@app.post("/api/projects", response_model=_schemas.Project)
async def create_project(
    project: _schemas._ProjectBase,
    admin: _schemas.User = _fastapi.Depends(_services.get_current_user), # need to be signed in for access.
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    return await _services.create_project(project=project,db=db)

@app.get("/api/projects", response_model=List[_schemas.Project])
async def get_projects(
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    return await _services.get_projects(db)

@app.delete("/api/projects/{project_id}", status_code=204)
async def delete_project(
    project_id: int,
    admin: _schemas.User = _fastapi.Depends(_services.get_current_user), # need to be signed in for access.
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):    
    await _services.delete_project(project_id, db)
    return {"message": "Successfully Deleted"}

@app.put("/api/projects/{project_id}", status_code=200)
async def update_project(
    project_id: int,
    project: _schemas._ProjectBase,
    admin: _schemas.User = _fastapi.Depends(_services.get_current_user), # need to be signed in for access.
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    await _services.update_project(project_id, project, db)
    return {"message": "Successfully Updated"}

@app.get("/api")
async def root():
    return {"message": "This Works"}