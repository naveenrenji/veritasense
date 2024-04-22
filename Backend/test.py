import requests
import time
import csv
from concurrent.futures import ThreadPoolExecutor

# Configuration
base_url = 'http://your-api-url.com'
login_endpoint = '/login'
chat_endpoint = '/chat'
users = [
    {"username": "user1", "password": "pass1"},
    {"username": "user2", "password": "pass2"},
    {"username": "user3", "password": "pass3"},
    {"username": "user4", "password": "pass4"},
    {"username": "user5", "password": "pass5"}
]

def login(user):
    """Function to simulate user login."""
    response = requests.post(f"{base_url}{login_endpoint}", json=user)
    return response.json()['token']  # Assuming a token is returned

def send_message(token, message):
    """Function to send a message."""
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(f"{base_url}{chat_endpoint}", json={"message": message}, headers=headers)
    return response.status_code

def simulate_user_interaction(user, num_messages=10):
    """Simulate a single user sending multiple messages."""
    start_time = time.time()
    token = login(user)
    for i in range(num_messages):
        send_message(token, f"Message {i+1} from {user['username']}")
    end_time = time.time()
    return end_time - start_time

def perform_test(num_users, num_messages):
    """Perform tests for a specific number of users and messages."""
    with ThreadPoolExecutor(max_workers=num_users) as executor:
        results = list(executor.map(lambda user: simulate_user_interaction(user, num_messages), users[:num_users]))
    return sum(results) / len(results)  # Average time

def main():
    results = []
    num_messages = 10
    for num_users in range(1, 6):  # From 1 to 5 users
        avg_time = perform_test(num_users, num_messages)
        results.append((num_users, num_messages, avg_time))
        print(f"Average time for {num_users} users sending {num_messages} messages each: {avg_time} seconds")
    
    # Save results to CSV
    with open('test_results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Number of Users', 'Number of Messages per User', 'Average Time (seconds)'])
        writer.writerows(results)

if __name__ == "__main__":
    main()
