from typing import List
import uuid
import fastapi
from beanie import Document, init_beanie
from pydantic import Field, BaseModel
import motor.motor_asyncio


class Message(Document):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    text: str
    secret_text: str


class MessageResponse(BaseModel):
    id: uuid.UUID
    text: str


app = fastapi.FastAPI()


@app.get("/", response_model=List[MessageResponse])
async def home():
    create_mess = Message(text="hey", secret_text="secret")
    await create_mess.insert()
    get_messes = await Message.find_all().to_list()
    return get_messes


user = "admin"
password = "adminpass"
host = "mongodb"
port = 27017
DATABASE_URL = f"mongodb://{user}:{password}@{host}:{port}"


@app.on_event("startup")
async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)
    await init_beanie(database=client.db_name, document_models=[Message])
