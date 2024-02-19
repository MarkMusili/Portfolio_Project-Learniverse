$(document).ready(function () {
    $(".user_input").submit(function (event) {
        event.preventDefault();

        const Prompt = $(".input").val();

        // if (!Prompt.trim()) {
        //     alert("Please enter your prompt");
        //     return;
        // }

        // Clear the input field
        $(".input").val("");

        ///show after successfull call
        $(".response").show();

        fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            body: JSON.stringify({ prompt: Prompt }),
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then((response) => response.json())
            .then((data) => {
                // $("ai-response").text(data)
                // console.log(data)
                json_data = JSON.parse(data)
            })
            .catch((error) => {
                console.error("Error:", error);
            });

        });
});