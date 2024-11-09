import os
from openai import OpenAI
import json

if len(os.environ.get("GROQ_API_KEY")) > 30:
    from groq import Groq
    model = "mixtral-8x7b-32768"
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
        )
else:
    OPENAI_API_KEY = os.getenv('OPENAI_KEY')
    model = "gpt-4o"
    client = OpenAI(api_key=OPENAI_API_KEY)

def generate_script(topic):
    prompt = (
        """Vous êtes un rédacteur de contenu expérimenté pour une chaîne YouTube Shorts, spécialisée dans les vidéos chrétiennes. 
        Vos vidéos de faits sont concises, chacune durant moins de 50 secondes (environ 140 mots). 
        Ils sont incroyablement attrayants et originaux. Lorsqu'un utilisateur demande un type spécifique de court métrage, vous le créez.

        Vous avez maintenant pour mission de créer le meilleur scénario court basé sur le type de 'histoires ou faits chrétiens' demandés par l'utilisateur.

        Il doit être bref, très intéressant et unique.

        Produisez strictement le script dans un format JSON comme ci-dessous, et ne fournissez qu'un objet JSON analysable avec la clé 'script'.

        # Output
        {"script": "Here is the script ..."}
        """
    )

    response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": topic}
            ]
        )
    content = response.choices[0].message.content
    try:
        script = json.loads(content)["script"]
    except Exception as e:
        json_start_index = content.find('{')
        json_end_index = content.rfind('}')
        print(content)
        content = content[json_start_index:json_end_index+1]
        script = json.loads(content)["script"]
    return script
