document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chat-form");
    const userInput = document.getElementById("user-input");
    const chatWindow = document.getElementById("chat-window");

    chatForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const userMessage = userInput.value.trim();
        if (!userMessage) return;

        // Display user's message
        addMessage(userMessage, "user");
        userInput.value = "";

        try {
            // Send message to the backend
            const response = await fetch("http://127.0.0.1:8002/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ question: userMessage }),
            });

            if (!response.ok) {
                throw new Error("Network response was not ok.");
            }

            const data = await response.json();
            
            // Display bot's response
            addMessage(data.answer, "bot");

        } catch (error) {
            console.error("Error:", error);
            addMessage("Sorry, something went wrong. Please try again.", "bot");
        }
    });

    function addMessage(message, sender) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message", `${sender}-message`);
        messageElement.textContent = message;
        chatWindow.appendChild(messageElement);
        chatWindow.scrollTop = chatWindow.scrollHeight; // Auto-scroll to the bottom
    }
});