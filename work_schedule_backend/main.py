from fastapi import FastAPI

from work_schedule_backend.db.core import Base, engine
from work_schedule_backend.routes import permission, user

app = FastAPI()


# Include routes from the user module
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(permission.router, prefix="/permissions", tags=["permissions"])


# Create tables in the database
async def startup_event() -> None:
    Base.metadata.create_all(bind=engine)


app.add_event_handler("startup", startup_event)


# Example endpoint to check if the API is running
@app.get("/")
def read_root() -> None:
    return {"message": "Hello, FastAPI"}
