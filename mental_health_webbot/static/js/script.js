document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const optionsContainer = document.getElementById('options-container');
    const inputBar = document.querySelector('.bg-white.p-4.border-t');

    let isMoodAssessmentActive = true; // Flag to control mood assessment phase

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') { // Allow sending message via enter during assessment
            sendMessage();
        }
    });

    function sendMessage(messageToSend = null) {
        let message;
        if (messageToSend) {
            message = messageToSend;
        } else {
            message = userInput.value.trim();
            if (message === '') return;
        }

        appendMessage(message, 'user-message');
        userInput.value = '';
        optionsContainer.innerHTML = ''; // Clear options after sending message
        optionsContainer.classList.add('hidden'); // Hide options container

        showTypingIndicator(); // Show typing indicator

        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            hideTypingIndicator(); // Hide typing indicator
            appendMessage(data.response, 'bot-message');

            if (data.options) {
                displayOptions(data.options);
            } else if (data.response.includes("Now, how can I help you with anything else?")) {
                isMoodAssessmentActive = false; // End mood assessment phase
                inputBar.classList.remove('hidden'); // Show input bar
            }
        })
        .catch(error => {
            hideTypingIndicator(); // Hide typing indicator even on error
            console.error('Error:', error);
            appendMessage('Oops! Something went wrong.', 'bot-message');
        });
    }

    function appendMessage(message, type) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('flex', 'mb-2', type === 'user-message' ? 'justify-end' : 'justify-start');
        
        const messageContentDiv = document.createElement('div');
        messageContentDiv.classList.add(
            'mt-2', 'mb-2', 'p-3', 'rounded-xl', 'shadow',
            type === 'user-message' ? 'bg-blue-200' : 'bg-teal-100',
            'text-gray-800', 'max-w-xs', 'lg:max-w-md'
        );
        messageContentDiv.innerHTML = `<p>${message}</p>`;
        
        messageDiv.appendChild(messageContentDiv);
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function displayOptions(options) {
        optionsContainer.innerHTML = ''; // Clear previous options
        optionsContainer.classList.remove('hidden'); // Show options container
        // inputBar.classList.add('hidden'); // Keep input bar visible during assessment

        options.forEach(option => {
            const button = document.createElement('button');
            button.textContent = option;
            button.classList.add(
                'bg-purple-200', 'text-purple-800', 'px-4', 'py-2', 'rounded-full',
                'hover:bg-purple-300', 'focus:outline-none', 'focus:ring-2', 'focus:ring-purple-500',
                'focus:ring-opacity-50', 'text-sm'
            );
            button.addEventListener('click', () => sendMessage(option));
            optionsContainer.appendChild(button);
        });
    }

    // Fetch and display the initial question when the page loads
    fetch('/get_initial_question')
        .then(response => response.json())
        .then(data => {
            appendMessage(data.question, 'bot-message');
            if (data.options) {
                displayOptions(data.options);
            }
        })
        .catch(error => {
            console.error('Error fetching initial question:', error);
            appendMessage('Hello! How can I help you today?', 'bot-message');
            isMoodAssessmentActive = false; // Ensure input bar is visible if initial question fails
            inputBar.classList.remove('hidden');
        });

    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('flex', 'mb-2', 'justify-start');
        typingDiv.id = 'typing-indicator';
        
        const typingContentDiv = document.createElement('div');
        typingContentDiv.classList.add(
            'mt-2', 'mb-2', 'p-3', 'rounded-xl', 'shadow',
            'bg-teal-100', 'text-gray-800', 'max-w-xs', 'lg:max-w-md'
        );
        typingContentDiv.innerHTML = `
            <div class="typing-indicator flex items-center space-x-1">
                <span class="h-2 w-2 bg-gray-500 rounded-full animate-pulse"></span>
                <span class="h-2 w-2 bg-gray-500 rounded-full animate-pulse delay-75"></span>
                <span class="h-2 w-2 bg-gray-500 rounded-full animate-pulse delay-150"></span>
                <span class="ml-2">Mitra is typing...</span>
            </div>
        `;
        
        typingDiv.appendChild(typingContentDiv);
        chatBox.appendChild(typingDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function hideTypingIndicator() {
        const typingDiv = document.getElementById('typing-indicator');
        if (typingDiv) {
            typingDiv.remove();
        }
    }


});