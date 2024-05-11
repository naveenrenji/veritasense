To set up and start the backend 

1. If not already existsing - create a virtual environment for your project:

     python3 -m venv newenv

2.  On Windows: 

        newenv\Scripts\activate

    On Unix or MacOS: 
    
        source newenv/bin/activate

3. Install libraries in your virtual environment: 

     pip install -r requirements.txt

     python -m spacy download en_core_web_sm


4. Run your Flask app:

Before running your Flask application, you need to set the FLASK_APP environment variable:

    On Windows:

        set FLASK_APP=app.py

    On Unix or MacOS:

        export FLASK_APP=app.py

5. Start your Flask application by running:

        flask run

Your API will be available at http://localhost:5000.


6. docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama


6. To install llama3 from ollama - curl -fsSL https://ollama.com/install.sh | sh

7. to start ollama - ollama run llama3


to make sure ollama and backend are on same network - 

Step 1: Ensure Both Containers Are on the Same Network
Since your Docker network listing did not show a custom network that includes both your backend and the Ollama service, you should either create a new custom network or make sure both are on the same default network with proper settings. Here’s how to create and connect them to a custom network:

Create a Custom Network (if not already done):

bash
Copy code
docker network create --driver bridge app_network
Connect Both Containers to the New Network:

bash
Copy code
docker network connect app_network great_perlman
docker network connect app_network ollama
Step 2: Confirm Network Connection
After connecting both services to the same network, check again to ensure they are correctly attached:

bash
Copy code
docker inspect great_perlman | grep -i "networks"
docker inspect ollama | grep -i "networks"
This will confirm that both containers are on the app_network.

Step 3: Use the Correct Hostname in Backend Code
Make sure that in your backend Docker container, you are using the correct service name as the hostname in your connection URL to the Ollama service. This should match the service name specified in your Docker network setup:

python
Copy code
import requests

url = "http://ollama:11434/api/chat"
response = requests.post(url, json={"model": "llama3", "messages": messages, "stream": True})
Step 4: Test the Connection
You can test the connection by running a simple curl command from within your great_perlman backend container to the Ollama service:

bash
Copy code
docker exec -it great_perlman curl http://ollama:11434
If curl is not installed, you can install it temporarily or use a Python script as mentioned previously to perform the test.
