let chatId = null;

const chatContainerDiv = document.getElementById('chat-container');
const messageInput = document.getElementById('message-input');

document.getElementById('message-send-btn').addEventListener('click', async () => {
    const messageContent = messageInput.value;
    if (messageContent == '') return;
    messageInput.value = '';

    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', 'user');
    messageDiv.append(messageContent);
    chatContainerDiv.appendChild(messageDiv);
    if (chatId === null) {
        await fetch('/api/chat/new', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4MDQwMTY0NCwianRpIjoiMWUzMzIzOGMtNTZkYy00NGM4LWEyZjQtNmIxNGNhOTBmMjUwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjgwNDAxNjQ0LCJleHAiOjE2ODI5OTM2NDR9.XqMMleY_OKd6WIHKpPSJm55oIfa4y38fVx6njxOTAzQ'
            },
        })
        .then(resp => resp.json())
        .then(json => {
            console.log(json);
            chatId = json.data.chat_id;
        });
    }

    const response = await fetch('/api/chat/message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4MDQwMTY0NCwianRpIjoiMWUzMzIzOGMtNTZkYy00NGM4LWEyZjQtNmIxNGNhOTBmMjUwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjgwNDAxNjQ0LCJleHAiOjE2ODI5OTM2NDR9.XqMMleY_OKd6WIHKpPSJm55oIfa4y38fVx6njxOTAzQ'
        },
        body: JSON.stringify({chat_id: chatId, content: messageContent}),
    });
    const reader = response.body.getReader();
    const responseDiv = document.createElement('div');
    responseDiv.classList.add('message', 'system');
    chatContainerDiv.appendChild(responseDiv);
    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        let valueDecoded = new TextDecoder().decode(value);
        responseDiv.append(valueDecoded);
    }
})
