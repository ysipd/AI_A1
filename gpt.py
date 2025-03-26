# from fastapi import FastAPI, HTTPExeption
from pydantic import BaseModel
import openai
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()  # Load environment variables from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

def classify_conversation(conversation_id, conversation):
    system_prompt = """
    You are an AI trained to analyze chatbot conversations for a rental website.
    Your task is to classify each conversation as 'Successful' or 'Unsuccessful' based on the bot's responses.

    ### Classification Criteria:
    1. **Successful Conversation:**
       - The bot provides a relevant and clear response to the user's request.
       - If the user's request cannot be fulfilled due to unavailable requirements or limitations, and the bot correctly informs the user about this unavailability, the conversation should still be considered successful. The success of the conversation is determined by the accuracy and relevance of the bot's response, not merely by the availability of the requested information or service. As long as the bot provides a truthful and appropriate response, acknowledging the limitations, the conversation remains valid and successful.
       Also when a user asks of something, bot may follow some steps and try to get input from user, and if user fails to give correct input then bot again asks for valid input, this is a successful conversation.

       for example:
        - 
        - If a requested flat is available, the bot provides details. It is successful.
        - If a requested flat is NOT available, but the bot properly informs the user, it is still successful.

    2. **Unsuccessful Conversation:**
       - The bot does not respond to the user's query.
       - The bot provides incorrect, unclear, or irrelevant responses.
       - The bot fails to acknowledge the user's request.
       - An unsuccessful conversation occurs when the bot fails to provide a correct, relevant, or meaningful response to the user's request. This can happen if the bot gives incorrect or misleading information, responds vaguely or incompletely, fails to acknowledge constraints, does not respond at all due to technical issues, repeats itself without addressing the user's intent, or provides irrelevant or off-topic replies. In essence, a conversation is unsuccessful when the bot does not effectively guide, inform, or assist the user in a meaningful way.
       - if the user asks for an agent or person to talk to, then its unsucessful reguardless of rest of the conversation.
       - if bot is unable to listen/hear or understand user then its an unsuccessful conversation
       - if bot leaves user query or message without responding then its unsuccessful.
       - if bot fails to address user query when asked for 1st time but it gives valid response when asked same query 2nd time, still it will be an unsuccessful.because bot failed ti address it when asekd for 1st tme itself.
       - If the bot provides any misunderstanding, fallback phrase, or incorrect response at any point in the conversation, even if it later corrects itself, classify it as 'unsuccessful'. The bot must respond correctly on the first attempt for the conversation to be considered 'successful'.
       - if bot says  I am a virtual assistant and did not understand, its unsuccessful.

     ### Confidence Score Calculation:
    - Provide a **confidence score** (between **0.0 and 1.0**) based on with how much confidence you think this conversation is successful or unsuccessful 
      
    **Response Format (JSON Only):**
    {{
        "conversation id": the respective conversation id, 
        "conversation": the conversation,
        "label": "successful" or "unsuccessful",
        "confidence": float (between 0 and 1),
        "reason": "Explain why the conversation was classified as successful or unsuccessful"
    }}

    
    
    """

    user_prompt = f"Analyze the following chatbot conversation:\n\n{conversation}\n\nClassify the conversation as successsful or unsuccessful."


    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        temperature = 0.0,
        # response_format="json_object",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"}

    )

    # result = response
    result = response.choices[0].message.content

    result_cleaned = re.sub(r"```(?:json|python)?\n(.*?)\n```", r"\1", result, flags=re.DOTALL).strip()
    # print(result)
    # result_json = json.loads(result)
    try:
        result_json = json.loads(result_cleaned)
        result_json["conversation id"] = conversation_id
        # result_json["conversation"] = conversation.replace("<br>","\n  ").splitlines()
    except json.JSONDecodeError:
        return {
            "conversation_id": conversation_id,
            "conversation": conversation,
            "label": "Unsuccessful",
            "confidence": 0.0,
            "error": f"Invalid JSON format: {result}"
        }

    return result_json


    # return result
    # Return the result in python dictionary format:
    # {
    #     "conversation id": the respective conversation id, 
    #     "conversation": the conversation,
    #     "label": "Successful or unsuccessful",
    #     "confidence": confidense score of beign successful or unsuccessful
    # }


   


