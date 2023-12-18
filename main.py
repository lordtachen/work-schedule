from fastapi import FastAPI
from app.routes import user
from app.db.session import Base, engine


app = FastAPI()

# Include routes from the user module
app.include_router(user.router, prefix="/users")

# Create tables in the database
Base.metadata.create_all(bind=engine)


# Example endpoint to check if the API is running
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI"}
