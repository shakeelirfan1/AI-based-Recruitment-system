import json

class JSONParser:

    def clean_json(self, text):

        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

        return json.loads(text)