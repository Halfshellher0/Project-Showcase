import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import jwt as _jwt
import database as _database
import models as _models
import schemas as _schemas

oauth2schema = _security.OAuth2PasswordBearer(tokenUrl="/api/token")

JWT_SECRET = "YmI0C02320Kc20P4r80u" # TODO move to .env

def init_db():
    return _database.Base.metadata.create_all(bind=_database.engine)

def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_user_by_username(username: str, db: _orm.Session) -> _models.User:
    return db.query(_models.User).filter(_models.User.username == username).first()

async def create_user(user: _schemas.UserCreate, db: _orm.Session) -> _models.User:
    user_obj = _models.User(username=user.username, hashed_password=_hash.bcrypt.hash(user.password))
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj

async def authenticate_user(username:str, password: str, db: _orm.Session):
    user = await get_user_by_username(username, db)

    if not user:
        return False

    if not user.verify_password(password):
        return False
        
    return user

async def create_token(user: _models.User):
    user_obj = _schemas.User.from_orm(user)
    token = _jwt.encode(user_obj.dict(), JWT_SECRET)
    return dict(access_token=token, token_type="bearer")

async def get_current_user(token: str = _fastapi.Depends(oauth2schema), db: _orm.Session = _fastapi.Depends(get_db)):
    try:
        payload = _jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(_models.User).get(payload["id"])
    except:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid username or password")
    
    return _schemas.User.from_orm(user)

async def create_project(project: _schemas.Project, db: _orm.Session):
    project = _models.Project(**project.dict())
    db.add(project)
    db.commit()
    db.refresh(project)
    return _schemas.Project.from_orm(project)

async def get_projects(db: _orm.Session):
    projects = db.query(_models.Project).all()

    return list(map(_schemas.Project.from_orm, projects))

async def _project_selector(project_id: int, db: _orm.Session):
    project = db.query(_models.Project).filter(_models.Project.id == project_id).first()
    
    if project is None:
        raise _fastapi.HTTPException(status_code=404, detail="Project does not exist")

    return project

async def delete_project(project_id: int, db: _orm.Session):
    project = await _project_selector(project_id, db)

    db.delete(project)
    db.commit()

async def update_project(project_id: int, project: _schemas._ProjectBase, db: _orm.Session):
    project_db = await _project_selector(project_id, db)

    project_db.name = project.name
    project_db.description = project.description
    project_db.github = project.github
    project_db.iconPath = project.iconPath

    db.commit()
    db.refresh(project_db)

    return _schemas.Project.from_orm(project_db)

