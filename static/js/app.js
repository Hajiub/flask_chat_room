/* Creating new instace of io and assing it the socketio var! */
let socketio = io();
/* Listening for the "send-bth" button to be click in the dom */
const sendMessage = document.getElementById('send-btn');

// Get the messages container element
const messagesContainer = document.getElementById('messages');

// Function to create a new message
const createMessage = (name, message) => {
  const currentDate = new Date().toLocaleString();
  const messageTemplate = `
    <div class="text">
      <span><strong>${name}</strong>: ${message}</span>
      <span class="muted">${currentDate}</span>
    </div>
  `;
  messagesContainer.insertAdjacentHTML('beforeend', messageTemplate);
};
socketio.on('message',(data) => {
    createMessage(data.name,data.message);
});


function sendMessageHandler() {
  const messageInput = document.getElementById('MyInput');
  if (messageInput.value === '') return;
  socketio.emit('message', { data: messageInput.value });
  messageInput.value = '';
}

sendMessage.addEventListener('click', sendMessageHandler);



