const messageInput =
    document.getElementById("messageInput");

const sendButton =
    document.getElementById("sendButton");

const messages =
    document.getElementById("messages");


function addMessage(text, type) {
    const message =
        document.createElement("div");

    message.classList.add(
        "message",
        type
    );

    message.textContent = text;

    messages.appendChild(message);

    messages.scrollTop =
        messages.scrollHeight;
}


async function sendMessage() {
    const text = messageInput.value.trim();

    if (text === "") {
        return;
    }

    addMessage(
        `你：${text}`,
        "user-message"
    );

    messageInput.value = "";

    try {
        const response = await fetch(
            "/chat",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    message: text
                })
            }
        );

        const data = await response.json();

        addMessage(
            `机器人：${data.reply}`,
            "bot-message"
        );

    } catch (error) {
        addMessage(
            "机器人：请求失败，请稍后重试。",
            "bot-message"
        );

        console.error(error);
    }
}


sendButton.addEventListener(
    "click",
    sendMessage
);


messageInput.addEventListener(
    "keydown",
    function (event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    }
);