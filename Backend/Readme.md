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


