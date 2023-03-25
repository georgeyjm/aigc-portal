const messageInput = document.querySelector('.user-input input[type="text"]');
const sendButton = document.querySelector('.user-input button');
const messagesContainer = document.querySelector('.messages');

// Create a new message element
function createMessageElement(text, isUser) {
  const messageElement = document.createElement('div');
  const messageClass = isUser ? 'user-message' : 'system-message';
  messageElement.classList.add(messageClass);
  messageElement.innerText = text;
  return messageElement;
}

// Add a new message to the chat window
function addMessage(text, isUser) {
  const messageElement = createMessageElement(text, isUser);
  messagesContainer.appendChild(messageElement);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Handle sending a message
function sendMessage() {
  const text = messageInput.value.trim();
  if (text === '') return;
  addMessage(text, true);
  messageInput.value = '';
}

// Add event listeners
messageInput.addEventListener('keydown', event => {
  if (event.key === 'Enter') {
    event.preventDefault();
    sendMessage();
  }
});

sendButton.addEventListener('click', event => {
  event.preventDefault();
  sendMessage();
});
