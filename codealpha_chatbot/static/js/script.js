// script.js
document.getElementById('send-button').addEventListener('click', function() {
    var userInput = document.getElementById('user-input').value;
    if (userInput.trim() !== "") {
        displayMessage(userInput, 'user');
        getBotResponse(userInput);
        document.getElementById('user-input').value = '';
    }
});

document.getElementById('user-input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        document.getElementById('send-button').click();
    }
});

function displayMessage(message, sender) {
    var chatBox = document.getElementById('chat-box');
    var messageDiv = document.createElement('div');
    messageDiv.classList.add('chat-message');
    messageDiv.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
    messageDiv.textContent = message;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function getBotResponse(userMessage) {
    fetch(`/get?msg=${encodeURIComponent(userMessage)}`)
        .then(response => response.json())
        .then(data => {
            displayMessage(data.response, 'bot');
        });
}
