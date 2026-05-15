from services.agent import handle_chat

messages = [
    {"role": "user", "content": "I need assessment"},
]

response = handle_chat(messages)
print(response)

print("\n---\n")

messages = [
    {"role": "user", "content": "I want java developer test for 3 years experience"},
]

response = handle_chat(messages)
print(response)