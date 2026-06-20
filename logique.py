from openai import OpenAI
import json

client = OpenAI()


def analyser_requete(user_text):
    """
    ChatGPT transforme le texte en plan de dashboard
    """

    prompt = f"""
Tu es un expert data analyst.

Transforme ce texte en JSON STRICT.

Texte utilisateur :
{user_text}

Réponds UNIQUEMENT avec ce format :

{{
  "charts": [
    {{
      "type": "bar | line | pie",
      "x": "colonne",
      "y": "colonne",
      "groupby": "colonne"
    }}
  ]
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return json.loads(response.choices[0].message.content)
