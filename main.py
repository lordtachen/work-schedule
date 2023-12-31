from fastapi import FastAPI
from app.routes import user, permission
from app.db.session import Base, engine


app = FastAPI()

# Include routes from the user module
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(permission.router, prefix="/permissions", tags=["permissions"])

# Create tables in the database
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)


# Example endpoint to check if the API is running
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI"}
