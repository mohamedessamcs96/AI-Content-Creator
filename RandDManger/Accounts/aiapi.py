from openai import OpenAI



def content_writer_bot(user_input):
    # Construct the conversation
    try:
        client = OpenAI(api_key="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")
        print(client)
    except Exception as e:
        print("Error:", e)
        print("Please check your API key.")
    conversation = [
        {"role": "system", "content": "You are an assistant as a Content Writer."},
        {"role": "user", "content": user_input},
    ]

    try:
        # Send the conversation to OpenAI API
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation
        )

        # Print the generated message from the API response
        return completion.choices[0].message
    except Exception as e:
        print("Error:", e)
        return "An error occurred while processing your request."
