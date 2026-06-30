from groq import Groq

client = Groq(
    api_key="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"
)

def ask_ai(question):

    try:

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ]
        )

        return completion.choices[0].message.content

    except Exception as e:

        return f"Error: {str(e)}"