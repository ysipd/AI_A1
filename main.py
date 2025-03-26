from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import uvicorn
import pickle

import pandas as pd
from transformers import pipeline

app = FastAPI()

from single import get_response
from gpt import classify_conversation


@app.get("/Conversation/{ConversationId}")
async def get_convo(ConversationId: int):

    cid, conversation, predicted_label, confidence = get_response(ConversationId)
    
    response = {
        "ConversationId": int(cid),
        "Conversation": conversation.replace("<br>","\n  ").splitlines(),
        "result": predicted_label,
        "confidence_score": round(float(confidence),3)
    }
    return response



df = pd.read_pickle('convo4.pkl')

@app.get("/classify/{cid}")
def classify(cid: int):
    
    found = df[df['ConversationId'] == cid]
    if found.empty:
        raise HTTPException(status_code=404, detail='Conversation id not found')

    foundrow = found.iloc[0]
    conversation = foundrow['Conversation']
    # conversation = conversation.replace("<br>","\n  ").splitlines()

    classification = classify_conversation(cid, conversation)
    return classification


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)








# df = pd.read_pickle('bart.pkl')

# @app.get("/Conversation/{ConversationId}")
# async def get_convo(ConversationId: int):
#     result = df[df['ConversationId']==ConversationId]
#     if result.empty:
#         raise HTTPException(status_code=404, detail='Conversation id not found')
#     row = result.iloc[0]
#     # response = {'Conversation_id' : row['ConversationId'], 'Conversation':row['Conversation'], 'Result' : row['result'], 'Confidence': row['confidence_score']}
#     response = {
#         "ConversationId": int(row['ConversationId']),
#         "Conversation": row['Conversation'].replace("<br>","\n  ").splitlines(),
#         "result": str(row['result']),
#         "confidence_score": round(float(row['confidence_score']),3)
#     }
#     return response