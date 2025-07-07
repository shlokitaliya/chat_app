let socket = null;


async function openChat(element){
    const room_name = element.dataset.room
    const friendID = element.dataset.friendId
    const username = element.dataset.username
    const pictureUrl = element.dataset.pictureUrl
    // console.log(room_name,friendID,username)

    CURRENT_CHAT_FRIEND_ID = friendID; 

    document.getElementById('default_chat_box').classList.add("hidden");
    document.getElementById('chat_box').classList.remove("hidden");

    document.getElementById('chat-friend-name').textContent = username;
    document.getElementById('chat-friend-pic').src = pictureUrl

    const message_area = document.getElementById('messages-area');
    message_area.innerHTML = '';

    // fetch old messages of this chat
    try{
        const response = await fetch(`/chat/fetch_messages/${friendID}`);
        const messages = await response.json();

        messages.forEach( msg => {
            appendMessage(msg.message,msg.timestamp,msg.is_sender)
        });

        // scroll to bottom 
        message_area.scrollTop = message_area.scrollHeight;

    } catch (err){
        console.log("error loadind messages: "+ err);
    }



    // close any precious socket when a new user is selected
    if (socket) socket.close();

    // open new websocket connection
    // socket = new WebSocket(`ws://${window.location.host}/ws/chat/${room_name}`);
    
    const protocol = window.location.protocol === "https:" ? "wss" : "ws";
    socket = new WebSocket(`${protocol}://${window.location.host}/ws/chat/${room_name}`);

    // listen for incomming messages
    socket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        const is_sender = data.sender_id === CURRENT_USER_ID;

        // generate formatted timestamp
        const now = new Date();
        const timestamp = now.toLocaleString('en-IN',{
            day: '2-digit', month: 'short', year: 'numeric',
            hour: '2-digit', minute: '2-digit', hour12: true
        });
        
        appendMessage(data.message, timestamp, is_sender);
        message_area.scrollTop = message_area.scrollHeight;
    }
    socket.onclose = () => {
        console.warn("WebSocket closed. Retrying in 5 seconds...");
        setTimeout(connectWebSocket, 5000); // Retry after 5 seconds
    };

};


// Submit message via form
document.getElementById('chat-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const input = document.getElementById('message-input');
    const message = input.value.trim();

    if (!message || !socket || !CURRENT_CHAT_FRIEND_ID) return;

    socket.send(JSON.stringify({
        message: message,
        chat_type: "Private_chat",
        receiver_id: CURRENT_CHAT_FRIEND_ID
    }));

    input.value = '';
});

function appendMessage(messageText, timestamp, isSender) {
    const messagesArea = document.getElementById("messages-area");

    const wrapper = document.createElement("div");
    wrapper.className = "flex flex-col " + (isSender ? "items-end" : "items-start");

    const bubble = document.createElement("div");
    bubble.className = (isSender
        ? "bg-blue-100 text-gray-900"
        : "bg-white text-gray-800") + " p-3 rounded-lg shadow-md max-w-xs";
    bubble.innerHTML = `<p class="text-sm">${messageText}</p>`;

    const time = document.createElement("span");
    time.className = "text-xs text-gray-500 mt-1";
    time.textContent = timestamp;

    wrapper.appendChild(bubble);
    wrapper.appendChild(time);
    messagesArea.appendChild(wrapper);
}

