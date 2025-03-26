import pandas as pd
from sklearn.metrics import accuracy_score
from gpt import classify_conversation

# Load test set
test_df = pd.read_csv('test_set.csv')  # Ensure it has 'conversation_id' and 'label' columns
df = pd.read_pickle('convo4.pkl')

predictions = []

for _, row in test_df.iterrows():
    conversation_id = row['conversationid']
    actual_label = row['label']

    # Retrieve conversation text
    found = df[df['ConversationId'] == conversation_id]
    if found.empty:
        continue  # Skip if conversation ID is not found

    conversation = found.iloc[0]['Conversation']

    # Get GPT prediction
    classification = classify_conversation(conversation_id, conversation)
    # print(classification)
    # classification = json.loads(classification)

    # Convert predicted label to numeric
    predicted_label = 1 if classification['label'] == "successful" else 0

    # Store results
    predictions.append({
        "conversation_id": conversation_id,
        "conversation": conversation.replace("<br>","\n  ").splitlines(),
        "actual_label": actual_label,
        "predicted_label": predicted_label,
        "classification": classification["label"],
        "confidence": classification["confidence"],
        "reason" : classification["reason"]
    })

# Convert to DataFrame
results_df = pd.DataFrame(predictions)

# Calculate accuracy
accuracy = accuracy_score(results_df['actual_label'], results_df['predicted_label'])

# Save results
results_df.to_csv("classification_results.csv", index=False)

print(f"Model Accuracy: {accuracy:.2%}")
