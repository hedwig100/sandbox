const port = 3000;
const socket = io(`http://localhost:${port}`,{
    withCredentials: true,
});

function appendMessage(message) {
    const messageElement = document.createElement('div');
    messageElement.innerText = message;
    document.getElementById('message-container').append(messageElement);
}

const name = prompt('What is your name?');
socket.emit('new-user', name);
appendMessage('You joined');

socket.on('user-connected', name => {
    appendMessage(`${name} connected`);
})

socket.on('chat-message', data => {
    appendMessage(`${data.name}: ${data.message}`);
})

socket.on('user-disconnected', name => {
    appendMessage(`${name} disconnected`);
})

// Send a chat message
const messageForm = document.getElementById('send-container');
const messageInput = document.getElementById('message-input');

messageForm.addEventListener('submit', e => {
    e.preventDefault();
    const message = messageInput.value;
    appendMessage(`You: ${message}`);
    socket.emit('send-chat-message', message);
    messageInput.value = '';
});