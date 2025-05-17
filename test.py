import requests

API_KEY = "sk-380c4d11157f429485c6b8c8960ab99a"  # Replace with yours!
response = requests.post(
    "https://api.deepseek.com/v1/chat/completions",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": "Hello"}]
    }
)
print(response.status_code, response.text)  # Output: 200 (success) or 401 (failure)