const chatLog = document.getElementById('chat-log');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

let typingTimer;
const typingDelay = 1000; // 1 second delay
let isTypingIndicatorShown = false; // flag to track if the typing indicator is shown

// function to append a new message to the chat log
function appendMessage(sender, message) {
    const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }); // Corrected line
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message', `${sender}-message`);

    const messageContent = document.createElement('div');
    messageContent.classList.add('message-content');
    messageContent.innerHTML = `${message}<br><small class="text-muted">${timestamp}</small>`;

    messageElement.appendChild(messageContent);
    chatLog.appendChild(messageElement);
    chatLog.scrollTop = chatLog.scrollHeight;
}

// function to show the typing indicator
function showTypingIndicator() {
    if (!isTypingIndicatorShown) {
        const typingIndicator = document.createElement('div');
        typingIndicator.classList.add('typing-indicator');
        typingIndicator.innerHTML = 'typing...';
        chatLog.appendChild(typingIndicator);
        chatLog.scrollTop = chatLog.scrollHeight;
        isTypingIndicatorShown = true;
    }
}

// function to hide the typing indicator
function hideTypingIndicator() {
    const typingIndicators = document.querySelectorAll('.typing-indicator');
    typingIndicators.forEach(indicator => {
        chatLog.removeChild(indicator);
    });
    isTypingIndicatorShown = false;
}

//  listener for 'click' event on the send button
sendButton.addEventListener('click', sendMessage);

//  listener for 'keypress' event on the user input field
userInput.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

//  listener for 'input' event on the user input field (for typing indicator)
userInput.addEventListener('input', () => {
    clearTimeout(typingTimer);
    showTypingIndicator();
    typingTimer = setTimeout(() => {
        hideTypingIndicator();
    }, typingDelay);
});

// send a message ke liye
async function sendMessage() {
    const userMessage = userInput.value;
    if (userMessage.trim() === '') return;

    appendMessage('user', userMessage);
    userInput.value = '';
    hideTypingIndicator(); // indicator hide when the message is sent

    try {
        const response = await fetch('/get_schedule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'user_input=' + encodeURIComponent(userMessage),
        });
        const data = await response.json();
        appendMessage('bot', data.response);
    } catch (error) {
        appendMessage('bot', 'Sorry, there was an error fetching your schedule. Please try again later.');
        console.error('Error fetching schedule:', error);
    }
}

// greeting bot message
appendMessage('bot', 'hello! our Routine Bot! How can I assist you with your college 😁schedule today?');