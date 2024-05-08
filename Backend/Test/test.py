import requests
import time
import csv
from concurrent.futures import ThreadPoolExecutor

base_url = 'http://155.246.39.38:5000'
signup_endpoint = '/auth/signup'
login_endpoint = '/auth/login'
logout_endpoint = '/auth/logout'
chat_endpoint = '/chat'
users = [
    {"name": "user1", "email": "user1@example.com", "password": "pass1"},
    {"name": "user2", "email": "user2@example.com", "password": "pass2"},
    {"name": "user3", "email": "user3@example.com", "password": "pass3"},
    {"name": "user4", "email": "user4@example.com", "password": "pass4"}
    # {"name": "user5", "email": "user5@example.com", "password": "pass5"}
]

messages = [
    "Can you provide an example of how to use the open() function to read from a text file in Python?",
    "Why do I need to initialize a list containing words with a hashtag and stop the loop into the file?",
    "What does the split function do when no separator is specified in the parentheses?",
    "Can you explain the purpose of the strip function in Python?",
    "How is a CSV file typically processed in Python?",
    "How can you split a string using a comma as the separator?",
    "What is the purpose of the `strip` method in Python?",
    "Why is it necessary to close a file after writing in Python?",
    "What are the characteristics of lists and tuples in Python?",
    "What are the main differences between lists and tuples in Python?"
]


def signup(user):
    response = requests.post(f"{base_url}{signup_endpoint}", json=user)
    return response.status_code

def login(user):
    response = requests.post(f"{base_url}{login_endpoint}", json=user)
    return response.json()['session_token'] 

def logout(token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(f"{base_url}{logout_endpoint}", headers=headers)
    return response.status_code

def send_message(token, message):
    """Function to send a message."""
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(f"{base_url}{chat_endpoint}", json={"message": message}, headers=headers)
    return response.json()  
    # return "test"

def simulate_user_interaction(user, messages):
    print("started single user for user ", user["name"])
    user_times = {'signup_time': 0, 'login_time': 0, 'message_times': [], 'logout_time': 0, 'messages_responses': []}
    start_time = time.time()
    signup_status = signup(user)
    user_times['signup_time'] = time.time() - start_time

    start_time = time.time()
    token = login(user)
    user_times['login_time'] = time.time() - start_time

    for message in messages:
        start_time = time.time()
        response = send_message(token, message)
        user_times['message_times'].append(time.time() - start_time)
        user_times['messages_responses'].append((message, response))

    start_time = time.time()
    logout_status = logout(token)
    user_times['logout_time'] = time.time() - start_time
    print("completed single user for user ", user["name"])

    return user_times

def perform_test(users, messages):
    all_user_times = []
    with ThreadPoolExecutor(max_workers=len(users)) as executor:
        user_times_list = list(executor.map(lambda user: simulate_user_interaction(user, messages), users))
        all_user_times.extend(user_times_list)

    average_response_time = sum(sum(user_times['message_times']) for user_times in all_user_times) / sum(len(user_times['message_times']) for user_times in all_user_times)

    with open('test_results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for i, user_times in enumerate(all_user_times, start=1):
            row = [f"user {i}", user_times['signup_time'], user_times['login_time']] + user_times['message_times'] + [sum(user_times['message_times']), user_times['logout_time']]
            for message, response in user_times['messages_responses']:
                row.extend([message, response])
            writer.writerow(row)

        writer.writerow(['Average Response Time', average_response_time])

if __name__ == "__main__":
    perform_test(users, messages)
