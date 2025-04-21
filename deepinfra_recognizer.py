# pip install requests
import base64
from pathlib import Path

import requests


INPUT_FILE = Path('test.png')
OUTPUT_FILE = Path('output_gemma.txt')
MODEL = "google/gemma-3-27b-it"
TEMPERATURE = 0.1
API_KEY = '<YOUR_DEEPINFRA_API_KEY>'
BASE_URL = 'https://api.deepinfra.com'


def encode_image_to_base64(image_path: Path) -> str:
    """Encode image to base64"""
    with image_path.open(mode='rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def main() -> None:
    base64_image = encode_image_to_base64(image_path=INPUT_FILE)

    response = requests.post(
        f'{BASE_URL}/v1/openai/chat/completions',
        headers={
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        },
        json={
            "model": MODEL,
            "temperature": TEMPERATURE,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text",
                         "text": "Extract all the text from this image. Return only the raw text, without any additional explanations."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ]
        }
    )
    if response.status_code != 200:
        raise ValueError(f'Status code != 200 {response.status_code} {response.content}')

    image_text_data = response.json()['choices'][0]['message']['content']

    with OUTPUT_FILE.open(mode='w', encoding='utf-8') as out_file:
        out_file.write(image_text_data)


if __name__ == '__main__':
    main()
