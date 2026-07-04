from fastapi import raiseExceptions
from fastapi import FastAPI, WebSocket, Request, HTTPException
import uvicorn
import logging

logging.basicConfig(
    format="%(asctime)s.%(msecs)03dZ %(levelname)s:%(name)s:%(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
    level=logging.INFO,
)
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
logging.getLogger("uvicorn.error").setLevel(logging.WARNING)

app = FastAPI()

clients = {}
subscribers = {}

@app.post("/webhook/{subscription_id}")
async def webhook(subscription_id: str, request: Request):
    if subscription_id is not None:
        header_val = request.headers.get("X-API-Key")
        if (header_val != "hello"):
            raise HTTPException(status_code=403, detail="API key is not valid ")

        data = await request.json()
        logging.info("Webhook received: %s", data)

        subscribers[subscription_id] = data
        client = clients.get(subscription_id)

        if client is not None:
            await client.send_json(data) 
            print("Data sent to websocket client")
        return {"message":"received"}  
     
    else:   
        print("Invalid endpoint, connection not accepted")
        return
    
    
@app.websocket("/tunnel/{subscription_id}")
async def websocket_endpoint(subscription_id: str, websocket: WebSocket):
    await websocket.accept()
    clients[subscription_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text("Message received")
    except Exception as e:
        clients.pop(subscription_id, None)


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=5000) 
    