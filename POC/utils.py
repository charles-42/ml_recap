def get_spotify_token():
    import requests
    import base64
    from dotenv import load_dotenv
    import os

    load_dotenv()
    ID = os.getenv('ID')
    PSW = os.getenv('PSW')

    # Step 1 - Authorization 
    url = "https://accounts.spotify.com/api/token"
    headers = {}
    data = {}

    # Encode as Base64
    message = f"{ID}:{PSW}"
    messageBytes = message.encode('ascii')
    base64Bytes = base64.b64encode(messageBytes)
    base64Message = base64Bytes.decode('ascii')


    headers['Authorization'] = f"Basic {base64Message}"
    data['grant_type'] = "client_credentials"

    r = requests.post(url, headers=headers, data=data)

    token = r.json()['access_token']

    return token

if __name__ == "__main__":
    print(get_spotify_token())