$(".user_input").submit(function (event) {
    event.preventDefault();

    const Prompt = $("#input").val();

    if (!Prompt.trim()) {
        alert("Please enter your prompt");
        return;
    }

    const History = $(".Chat-History");
    const User_message = $("<li></li>").addClass("user-message").text(Prompt);
    History.append(User_message);

    // Clear the input field
    $("#input").val("");

    const AI_message = $("<li></li>").addClass("bot-message").text("Loading...");
    History.append(AI_message);

    fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        body: JSON.stringify({ prompt: Prompt }),
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((response) => response.json())
        .then((data) => {
            AI_message.text(data)
            console.log(data)
        })
        .catch((error) => {
            console.error("Error:", error);
        });
});