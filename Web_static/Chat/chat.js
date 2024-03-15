$(document).ready(function () {
    $(".user_input").submit(function (event) {
        event.preventDefault();

        const Prompt = $(".input").val();

        if (!Prompt.trim()) {
            alert("Please enter your prompt");
            return;
        }

        // Clear the input field
        $(".input").val("");

        ///show after successfull call
        $(".response").show();

        fetch("http://52.59.213.161:8080/chat", {
            method: "POST",
            body: JSON.stringify({ prompt: Prompt }),
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then((response) => {
                if (response.ok) {
                    // Redirect to another page
                    window.location.href = "https://example.com/another-page";
                } else {
                    throw new Error("API request failed");
                }
            })
            .catch((error) => {
                console.error("Error:", error);
            });

        });
});