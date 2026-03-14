document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("send-btn").onclick = sendMessage;
    document.getElementById("user-input").addEventListener("keydown", e => {
        if (e.key === "Enter") sendMessage();
    });
});

async function sendMessage() {
    const input = document.getElementById("user-input");
    const chatBody = document.getElementById("chat-body");
    const language = document.getElementById("language").value;
    const message = input.value.trim();
    if (!message) return;

    chatBody.innerHTML += `<div class="user-message">${message}</div>`;
    const bot = document.createElement("div");
    bot.className = "bot-message";
    bot.innerText = "Typing...";
    chatBody.appendChild(bot);

    chatBody.scrollTop = chatBody.scrollHeight;
    input.value = "";

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ message, language })
        });
        const data = await res.json();
        bot.innerText = data.reply;
    } catch {
        bot.innerText = "❌ Server not reachable.";
    }
}
