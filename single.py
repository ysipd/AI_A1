import pandas as pd
from transformers import pipeline
from fastapi import FastAPI, HTTPException

# df = pd.read_pickle('convo3.pkl')
df = pd.read_pickle('convo4.pkl')


classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")


labels = ["successful", "unsuccessful"]

hypothesis_template2 = "This conversation is {} in satisfactorily answering the user's queries."
# hypothesis_template3 = "This conversation is {} in achieving a positive outcome for the user."


def get_response(cid: int):


    found = df[df['ConversationId'] == cid]
    if found.empty:
        raise HTTPException(status_code=404, detail='Conversation id not found')
    foundrow = found.iloc[0]
    conversation = foundrow['Conversation']

    result = classifier(conversation, labels, hypothesis_template=hypothesis_template2)

    predicted_label = result['labels'][0]
    confidence = result['scores'][0]

    return cid, conversation, predicted_label, confidence
