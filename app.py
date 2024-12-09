from fastapi import FastAPI, File, UploadFile
from pymongo import MongoClient
import openai, config
from datetime import datetime
import io
from bson.objectid import ObjectId

app = FastAPI()
openai.api_key = config.OPENAI_API_KEY

class NamedBytesIO(io.BytesIO):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name

# Route to handle file uploads
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    # Save file to disk
    contents = await file.read()
    audio_file = NamedBytesIO('test.mp3', contents)
    # transcript = openai.Audio.transcribe("whisper-1", audio_file)
    # response = transcript["text"]

    connection_string = f"mongodb+srv://{config.MONGO_USER}:{config.MONGO_PW}@interview-database.ul5p73y.mongodb.net"
    # set up the client
    client = MongoClient(connection_string)

    # select the database
    db = client[config.MONGO_DB_NAME]

    # select the collection
    collection = db[config.MONGO_COLLECTION_NAME]

    timestamp = datetime.now().timestamp()

    test_insert = {
        '_id': str(ObjectId()),
        'timestamp': timestamp,
        'user_id' : 1,
        'interivew_id' : 1,
        'audio_bytes' : str(contents),
        # 'transcribed_text' : response
    }

    result = collection.insert_one(test_insert)
    print(result.inserted_id)
    return test_insert