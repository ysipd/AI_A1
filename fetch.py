import pandas as pd
from db_connect import get_connected
import html
import re
from bs4 import BeautifulSoup
import json

connection=get_connected()
cursor = connection.cursor()


def clean_text(text):
    
    if text is None:
        return ""  
 
    text = str(text).strip()
    text = text[5:].strip()

 
    try:
        if text.startswith("{") or text.startswith("["):
            parsed_text = json.loads(text)
            if isinstance(parsed_text, list):  
                return "bot : "+" ".join(item.get("text", "") for item in parsed_text if isinstance(item, dict))
            elif isinstance(parsed_text, dict):
                return "bot : "+" ".join(parsed_text.values())  
    except json.JSONDecodeError:
        pass
 
    if "<" in text and ">" in text:  
        soup = BeautifulSoup(text, "html.parser")
        text = soup.get_text(separator=" ")
 
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()

    text = "bot : "+text
 
    return text



def fetch2():
    cursor.execute("SELECT conversationid, CONCAT('user: ', message) AS message, conversationincomingtime AS timestamp FROM conversationincoming")
    incoming = cursor.fetchall()

    cursor.execute("SELECT conversationid, CONCAT('bot: ', message) AS message, conversationoutgoingtime AS timestamp FROM conversationoutgoing")
    outgoing = cursor.fetchall()
    

    df_incoming = pd.DataFrame(incoming, columns=["ConversationId", "Message", "Timestamp"])
    df_outgoing = pd.DataFrame(outgoing, columns=["ConversationId", "Message", "Timestamp"])


    df_outgoing['Message'] = df_outgoing["Message"].apply(clean_text)


    df_incoming["Timestamp"] = pd.to_datetime(df_incoming["Timestamp"])
    df_outgoing["Timestamp"] = pd.to_datetime(df_outgoing["Timestamp"])

    combined_df = pd.concat([df_incoming, df_outgoing])

    # maintain chronological order
    combined_df = combined_df.sort_values(by=["ConversationId", "Timestamp"])

    # Group by ConversationId and concatenate messages
    grouped_df = combined_df.groupby("ConversationId").agg({
        "Message": lambda x: "\n".join(x.fillna(""))
    }).reset_index()

    grouped_df.rename(columns={"Message": "Conversation"}, inplace=True)

    return grouped_df




df = fetch2()

df.to_pickle('convo4.pkl')

# for conversation_id in range(35100,35200):
#     if (df["ConversationId"] == conversation_id).any() :
#         conversations = df[df["ConversationId"] == conversation_id]["Conversation"].values[0]
 
#         print(f"\nConversation ID: {conversation_id}\n{conversations}")

# def parse_bot_response(message):
    
#     if message is None:
#         return "None"
#     if message.startswith("bot: ["):
#         message = str(message)
#         message = list(message[5:])
#         if 'text' in message[0]:
#             message = message[0]['text']
#         else:
#             # message=''
#             message=str(message)

    
#     return message



# def extract_text_from_html(message):
#     # if isinstance(message, list):  # Convert list to string
#     #     message = " ".join(str(item) for item in message)
#     if "<" in message and ">" in message:  
#         soup = BeautifulSoup(message, "html.parser")
#         return soup.get_text(separator=" ").strip()
#     return message