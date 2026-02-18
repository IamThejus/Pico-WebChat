let socket;
const username = window.currentUser;
console.log("Connecting as:", username);
socket = new WebSocket(`ws://${window.location.host}/ws/${username}`);

socket.onmessage = (event) => {
    const result = JSON.parse(event.data);

    // Handle error
    if (result.type === "error") {
        alert(result.data.log || "Username already exists");
        window.location.href = "/";
        return;
    }

    // Update active users list
    if (result.type === "active-users-list") {
        renderActiveUsers(result.data.users);
        return;
    }

    // Handle public message
    if (result.type === "message" && result.data.type === "public") {
        const messages = document.getElementById("messages");
        messages.innerHTML += `<div>${result.data.sender} : ${result.data.message}</div>`;
        messages.scrollTop = messages.scrollHeight;
        return;
    }
    


    // Handle private message
    if (result.type === "message" && result.data.type === "private") {
        const sender = result.data.sender;
        openMiniChat(sender, result.data.message);
    }
};

// Send public message
function sendMessage() {
    const messageInput = document.getElementById("messageInput").value.trim();
    if (!messageInput) return;

    socket.send(JSON.stringify({
        type: "public",
        message: messageInput
    }));

    document.getElementById("messageInput").value = "";
}

// Render clickable active users
function renderActiveUsers(users) {
    const activeUsersDiv = document.getElementById("active-users");
    activeUsersDiv.innerHTML = "";

    users.forEach(user => {
        if (user === username) return; // skip self
        const userDiv = document.createElement("div");
        userDiv.innerText = user;
        userDiv.style.cursor = "pointer";
        userDiv.onclick = () => openMiniChat(user);
        activeUsersDiv.appendChild(userDiv);
    });
}

// Open mini chat window
function openMiniChat(user, incomingMessage = null) {
    const container = document.getElementById("mini-chats-container");

    // Check if already exists
    let chatBox = document.getElementById(`mini-chat-${user}`);
    if (!chatBox) {
        chatBox = document.createElement("div");
        chatBox.id = `mini-chat-${user}`;
        chatBox.style.width = "250px";
        chatBox.style.height = "300px";
        chatBox.style.background = "white";
        chatBox.style.border = "1px solid #ccc";
        chatBox.style.borderRadius = "8px";
        chatBox.style.display = "flex";
        chatBox.style.flexDirection = "column";
        chatBox.style.boxShadow = "0 5px 15px rgba(0,0,0,0.1)";

        // Header
        const header = document.createElement("div");
        header.innerText = `Chat with ${user}`;
        header.style.background = "#4f46e5";
        header.style.color = "white";
        header.style.padding = "5px 10px";
        header.style.fontWeight = "bold";
        header.style.cursor = "pointer";
        header.onclick = () => chatBox.remove(); // close on click
        chatBox.appendChild(header);

        // Messages div
        const messagesDiv = document.createElement("div");
        messagesDiv.style.flex = "1";
        messagesDiv.style.padding = "10px";
        messagesDiv.style.overflowY = "auto";
        chatBox.appendChild(messagesDiv);

        // Input area
        const inputArea = document.createElement("div");
        inputArea.style.display = "flex";
        inputArea.style.padding = "5px";

        const input = document.createElement("input");
        input.type = "text";
        input.placeholder = "Type message";
        input.style.flex = "1";
        input.style.marginRight = "5px";

        const sendBtn = document.createElement("button");
        sendBtn.innerText = "Send";
        sendBtn.onclick = () => {
            const msg = input.value.trim();
            if (!msg) return;
            socket.send(JSON.stringify({
                type: "private",
                receiver: user,
                message: msg
            }));
            messagesDiv.innerHTML += `<div style="text-align:right; color:blue;">${msg}</div>`;
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
            input.value = "";
        };

        inputArea.appendChild(input);
        inputArea.appendChild(sendBtn);
        chatBox.appendChild(inputArea);

        container.appendChild(chatBox);
    }

    // Append incoming message if any
    if (incomingMessage) {
        const messagesDiv = chatBox.querySelector("div:nth-child(2)");
        messagesDiv.innerHTML += `<div style="color:red;">${user}: ${incomingMessage}</div>`;
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
}
