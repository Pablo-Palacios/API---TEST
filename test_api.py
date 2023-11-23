import requests
import uuid 

HTTP = "https://todo.pixegami.io/"


def test_can_call_http():
    get_http_response = requests.get(HTTP)
    assert get_http_response.status_code == 200


def test_can_create_task():
    playload = new_playload_task()
    create_task_response = create_task(playload)
    assert create_task_response.status_code == 200 

    data = create_task_response.json()
    #print (data)
    
    task_id = data ["task"] ["task_id"]
    task_id_response = get_task(task_id)
    assert task_id_response.status_code == 200 
    get_task_response = task_id_response.json()
    print(get_task_response)

 

    assert get_task_response["content"] == playload["content"]
    assert get_task_response["user_id"] == playload["user_id"]


def test_can_take_list_tasks():
    n = 3 
    playload = new_playload_task()
    for _ in range(n):
        response_create_task = create_task(playload)
        assert response_create_task.status_code == 200 

    user_id = playload ["user_id"]
    response_list_tasks = get_list_tasks(user_id)
    assert response_list_tasks.status_code == 200
    data = response_list_tasks.json()
    #print(data)

    tasks = data["tasks"]
    assert len(tasks) == n 
    print(tasks)


def test_can_update_task():
    playload = new_playload_task()
    create_task_response = create_task(playload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"] ["task_id"]

    new_playload = {
            "user_id": playload["user_id"],
            "task_id": task_id,
            "content": "update content",
            "is_done": True
                                }

    update_tasks_response = update_tasks(new_playload)
    assert update_tasks_response.status_code == 200

    
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200

    get_update_tasks = get_task_response.json()


    assert get_update_tasks ["content"] == new_playload["content"]
    assert get_update_tasks["user_id"] == new_playload["user_id"]

    print(get_update_tasks)




def test_can_delete_task():
    playload = new_playload_task()
    create_task_response = create_task(playload)
    assert create_task_response.status_code == 200 
    task = create_task_response.json()

    delete_task_response = delete_task(task)
    assert delete_task_response.status_code == 200

    comp_delete_task = delete_task_response.json()
    get_delete_task = get_task(comp_delete_task)
    assert get_delete_task.status_code == 404








############################################3########################333

def new_playload_task():
    user_id = f"test_user_{uuid.uuid4().hex}"
    content = f"test_content_{uuid.uuid4().hex}"
    return {
            "content": content,
            "user_id": user_id,
            "is_done": False
                                }

def create_task(playload):
    return requests.put(HTTP + "/create-task", json = playload)


def get_task(task_id): 
    return requests.get(HTTP + f"/get-task/{task_id}")

def get_list_tasks(user_id):
    return requests.get(HTTP + f"/list-tasks/{user_id}")


def update_tasks(playload):
    return requests.put(HTTP + "/update-task", json= playload) 


def delete_task(task_id):
    return requests.delete(HTTP + f"/delete-task/ {task_id}")

