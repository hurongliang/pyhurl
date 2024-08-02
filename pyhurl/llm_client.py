from openai import OpenAI
import os
from dotenv import load_dotenv
import re
import json
from ollama import Client


class LLMClient:
    load_dotenv()
    openai_key = os.getenv('PYHURL_OPENAI_API')
    openai_model = os.getenv('PYHURL_OPENAI_MODEL')
    openai_api_base = os.getenv('PYHURL_OPENAI_API_BASE')
    openai_client = OpenAI(api_key=openai_key, base_url=openai_api_base)

    ollama_host = os.getenv('PYHURL_OLLAMA_HOST', 'http://localhost:11434')
    ollama_model = os.getenv('PYHURL_OLLAMA_MODEL', 'llama2')
    ollama_client = Client(host=ollama_host)

    @classmethod
    def call_openai(cls, messages: list[dict], model=None):
        response = cls.openai_client.chat.completions.create(
            model=cls.openai_model if model is None else model,
            messages=messages,
            stream=False,
            temperature=0.5,
            tool_choice='auto',
            top_p=1)
        return response.choices[0].message.content

    @classmethod
    def call_ollama(cls, messages: list[dict], model=None):
        return cls.ollama_client.chat(model=model if model else cls.ollama_model, messages=messages)['message']['content']

    @classmethod
    def find_all_json_datas(cls, text) -> list[object]:
        if not text:
            return []
        try:
            return [json.loads(text)]
        except:
            matches = re.findall(r'```(?:.*?)\s*([\[\{])(.*?)```', text, re.DOTALL)
            if matches:
                try:
                    return [json.loads(''.join(match)) for match in matches]
                except:
                    return []
            else:
                return []