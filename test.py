import requests

url = "http://127.0.0.1:8080/api/jobs"
url_users_api = "http://127.0.0.1:8080/api/v2/users"
url_jobs_api = "http://127.0.0.1:8080/api/v2/jobs"

"""Блок проверки API для работ"""
print(requests.get(url).json())
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
print(requests.post(url, json={'team_leader_id': 1}).status_code) # 400 ошибка из-за отсутствия обязательных полей
print(requests.post(url, json={'team_leader_id': 1000}).status_code) # 400 ошибка из-за того, что team_leader_id 1000 не существует в базе данных
print(requests.post(url, json={'team_leader_id': -1}).status_code) # 400 ошибка из-за того, что team_leader_id -1 не может быть валидным id пользователя
print(response.status_code) # 200 если все нужные поля
print(requests.delete(url + f"/{1}").status_code) # 200 если удаление прошло успешно
print(requests.delete(url + f"/{1000}").status_code) # 404 ошибка из-за того, что задачи с id 1000 не существует в базе данных
print(requests.delete(url + f"/{-1}").status_code) # 404 ошибка из-за того, что задачи с id -1 не существует в базе данных
print(requests.put(url + f"/{1}", json={'job': 'Updated job'}).status_code) # 200 если обновление прошло успешно
print(requests.put(url + f"/{1000}", json={'job': 'Updated job'}).status_code) # 404 ошибка из-за того, что задачи с id 1000 не существует в базе данных
print(requests.put(url + f"/{-1}", json={'job': 'Updated job'}).status_code) # 404 ошибка из-за того, что задачи с id -1 не существует в базе данных
print(requests.get(url).json())

"""Блок проверки API для пользователей"""
print(requests.get(url_users_api).json())
print(requests.post(url_users_api, json={'name': 'John', 'email': 'john@example.com'}).status_code)
print(requests.delete(url_users_api + f"/{1}").status_code)

"""Блок проверки API для работ"""
print(requests.get(url_jobs_api).json())
print(requests.post(url_jobs_api, json={"team_leader_id" : "1",
                   "job" : "bruh",
                   "work_size" : 1,
                   "collaborators" : "me",
                   "is_finished" : True}).status_code)
print(requests.delete(url_jobs_api + f"/{2}").status_code) # 200
print(requests.delete(url_jobs_api + f"/{1000}").status_code) # job isn't exist
print(requests.delete(url_jobs_api + f"/{-1}").status_code) # job can't exist