function addMessage(text, sender) {
    const chatBox = document.getElementById("chat-box");
    const msgDiv = document.createElement("div");
    msgDiv.className = sender + "-msg";

    const bubble = document.createElement("div");
    bubble.className = "bubble " + sender;
    bubble.innerText = text;

    msgDiv.appendChild(bubble);
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMessage() {
    const input = document.getElementById("userInput");
    const text = input.value.trim();
    if (!text) return;

    addMessage(text, "user");
    input.value = "";

    fetch("/nlp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ command: text })
    })
    .then(res => res.json())
    .then(data => {
        const response =
            "Intent: " + data.response.intent +
            "\nName: " + data.response.entities.name +
            "\nCategory: " + data.response.entities.category +
            "\nFood: " + data.response.entities.food_habits +
            "\nScore: " + data.response.entities.score;

        addMessage(response, "bot");
    })
    .catch(() => {
        addMessage("❌ Error processing request", "bot");
    });
}
