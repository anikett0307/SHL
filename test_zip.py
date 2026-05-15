from services.agent import handle_chat

tests = [
    [
        {"role": "user", "content": "I need assessment"}
    ],
    [
        {"role": "user", "content": "Java developer test"},
        {"role": "assistant", "content": "Please specify"},
        {"role": "user", "content": "add personality test"}
    ],
    [
        {"role": "user", "content": "compare Java 8 and Core Java"}
    ]
]

for i, messages in enumerate(tests):
    print(f"\n===== TEST {i+1} =====\n")
    response = handle_chat(messages)
    print(response)