# Mental Health Webbot
This is a Flask-based chatbot designed to provide basic mental health support for students. It uses a simple intent-based system to respond to user queries.

## Project Structure
- `app.py`: Main Flask application entry point.
- `requirements.txt`: Python dependencies (Flask, NLTK).
- `utils.py`: Contains the NLP and chatbot logic for processing messages and generating responses.
- `config.py`: Stores configuration variables like the bot's name.
- `data/intents.json`: JSON file containing predefined intents, patterns, and responses for the chatbot.
- `templates/index.html`: The main HTML file for the chatbot's user interface.
- `static/css/style.css`: CSS file for styling the chatbot interface with a soothing color scheme.
- `static/js/script.js`: JavaScript file for handling client-side interactions, sending messages, and displaying responses.

## Setup and Run

1.  **Clone the repository (if applicable):**
    ```bash
    git clone <repository_url>
    cd mental_health_webbot
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    -   **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    -   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the Flask application:**
    ```bash
    python app.py
    ```

6.  **Access the chatbot:**
    Open your web browser and go to `http://127.0.0.1:5000/` (or the address shown in your terminal).

## Customization
-   **Bot Name:** Modify `config.py` to change the name of the chatbot.
-   **Intents:** Modify `data/intents.json` to add, remove, or change chatbot intents, patterns, and responses.
-   **Styling:** Adjust `static/css/style.css` to change the visual appearance.
-   **Logic:** Enhance `utils.py` for more complex NLP or response generation.

## Contributing
Feel free to contribute to this project by submitting issues or pull requests.