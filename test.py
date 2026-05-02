import requests

url = "http://127.0.0.1:8080/api/jobs"

print(requests.get(url).json())
print(requests.get(f"{url}/1").json())
print(requests.get(f"{url}/99999").status_code)
print(requests.get(f"{url}/abc").status_code)
print(requests.post(url, json={}).status_code)
print(requests.post(url, json={'team_leader_id': 1}).status_code)
response = requests.post(url, json={
    'team_leader_id': 1,
    'job': 'Test job',
    'work_size': 10,
    'collaborators': '2, 3',
    'start_date': '2024-01-01',
    'end_date': '2024-01-10',
    'is_finished': False
})
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")