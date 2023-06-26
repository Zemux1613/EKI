import requests
import json

# URL des Endpunkts
url = 'http://deine-domain.de/user/create'

# JSON-Request-Body
request_data = {
    "email": "example@example.com",
    "firstname": "John",
    "birthday": "1990-10-15",
    "lastname": "Doe",
    "university": "Example University",
    "studyProgram": "Computer Science",
    "notice": "Some notice",
    "role": "ADMIN",
    "akaTitle": "Mr.",
    "banned": False
}

# Header für den Content-Type auf 'application/json' setzen
headers = {'Content-Type': 'application/json'}

# POST-Request senden
response = requests.post(url, data=json.dumps(request_data), headers=headers)

# Response überprüfen
if response.status_code == 201:  # Erfolgreiche Erstellung des Benutzers
    print('Benutzer erfolgreich erstellt.')
else:
    print('Fehler beim Erstellen des Benutzers:', response.text)