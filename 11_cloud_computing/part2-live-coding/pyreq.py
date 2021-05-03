import requests

url = "https://6ihbhfpjt4.execute-api.us-east-1.amazonaws.com/dev/portfolio"

payload="{\"tickers\":[\"AAPL\",\"FB\",\"TSLA\", \"NVDA\",\"TWTR\"]}"
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
