
from openai import OpenAI
import json

client = OpenAI()


def analyser_requete(user_text):
    prompt = f"""
Tu es un data analyst.

Transforme ce texte en JSON pour dashboard.

Texte :
{user_text}

Réponds uniquement en JSON :
{{
  "charts": [
    {{
      "type": "bar",
      "groupby": "colonne",
      "metric": "CA"
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

    content = response.choices[0].message.content

    return json.loads(content)
