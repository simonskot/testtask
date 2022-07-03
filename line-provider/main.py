import uvicorn
from config import HOST, PORT

uvicorn.run("app:app", host=HOST, port=PORT)
