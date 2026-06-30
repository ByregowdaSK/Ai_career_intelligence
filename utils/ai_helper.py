from groq import Groq

client = Groq(
    api_key="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"
)

def ask_ai(question):

    try:

        chat_completion = client.chat.completions.create(

            messages=[

                {
                    "role": "system",
                    "content": """
You are an AI Career Assistant.

Help students with:
- Career guidance
- Resume tips
- Interview preparation
- Skill improvement
- Project ideas
- Learning roadmap

Give clean and professional answers.
"""
                },

                {
                    "role": "user",
                    "content": question
                }

            ],

            model="llama3-8b-8192"
        )

        return chat_completion.choices[0].message.content

    except Exception as e:

        return f"Error: {str(e)}"