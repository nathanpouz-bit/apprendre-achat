from openai import OpenAI
import json

client = OpenAI()


def analyser_requete(user_text):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Tu es un data analyst. Réponds uniquement en JSON."
            },
            {
                "role": "user",
                "content": user_text
            }
        ]
    )

    try:
        return json.loads(response.choices[0].message.content)
    except:
        return {
            "charts": [
                {
                    "type": "bar",
                    "groupby": "auto",
                    "metric": "CA"
                }
            ]
        }
