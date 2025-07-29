
        "top_p": 0.9,
        'max_new_tokens': 128,
    })

response = llm.invoke("What is the capital of India?")
print(response)