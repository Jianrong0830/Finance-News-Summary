import os
import requests
import dotenv
import time
import random

dotenv.load_dotenv()
API_KEY = os.getenv("API_KEY")
ENDPOINT = os.getenv("ENDPOINT")

headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY,
}

def ask_gpt(prompt, messages, max_retries=3, max_wait_time=60):
    payload = {
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": messages},
        ],
        "temperature": 0.2,
        "top_p": 0.95,
        "max_tokens": 16000
    }

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(ENDPOINT, headers=headers, json=payload)
            if response.status_code == 429:
                wait_time = min(max_wait_time, 20 * attempt + random.uniform(0, 10))
                print(f"超出端點每分鐘用量。嘗試第 {attempt} 次重試，等待 {wait_time:.2f} 秒後重試。")
                if attempt < max_retries:
                    time.sleep(wait_time)
                    continue
                else:
                    raise Exception("超過最大重試次數，請稍後再試。")
            response.raise_for_status()
            response_json = response.json()
            return response_json["choices"][0]["message"]["content"]
        except requests.RequestException as e:
            print(f"請求失敗（嘗試 {attempt} / {max_retries}）：{e}")
            if attempt < max_retries:
                wait_time = min(max_wait_time, 20 * attempt + random.uniform(0, 10))
                print(f"等待 {wait_time:.2f} 秒後重試...")
                time.sleep(wait_time)
            else:
                raise Exception(f"超過最大重試次數。最後一次錯誤：{e}")
        except KeyError:
            raise Exception(f"意外的回應結構：{response.text}")

    raise Exception("無法獲取 GPT 回應。")

if __name__ == "__main__":
    print(ask_gpt("您是協助人員尋找資訊的 AI 助理。", "你好"))
