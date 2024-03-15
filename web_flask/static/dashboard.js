// jQuery event handlers
$(document).ready(function() {
    // Function to display current date
    function displayCurrentDate() {
        var currentDate = new Date();
        var options = { month: 'long', day: 'numeric', year: 'numeric' };
        var formattedDate = currentDate.toLocaleDateString('en-US', options);
        $('.time').text(formattedDate);
    }
    displayCurrentDate();

    // function to toggle dark mode
    $('.mode-btn').click(function() {
        $('body').toggleClass('dark');
        $('html').toggleClass('dark');
        var imgElement = this.querySelector('img');
        if (imgElement.src.endsWith('Slider-dark-mode-right.png')) {
            imgElement.src = '../static/Images/Slider-dark-mode-left.png';
        } else {
            imgElement.src = '../static/Images/Slider-dark-mode-right.png';
        }
    });


    // Function to handle drag events
    function drag(event) {
        event.dataTransfer.setData("text", event.target.id);
    };
    
    // Function to allow dropping elements
    function allowDrop(event) {
        event.preventDefault();
    };
    
    // Function to handle the drop event
    function drop(event) {
        event.preventDefault();
        var roadmapId = event.dataTransfer.getData("text");
        console.log("Roadmap ID:", roadmapId);
        var roadmap = document.getElementById(roadmapId);
        console.log("Roadmap Element:", roadmap);
        var column = event.target.id;
        console.log("Column ID:", column);
        event.target.appendChild(roadmap); // Append to the target element, not $(this)
        if (roadmap) {
            var columnElement = document.getElementById(columnId);
            columnElement.appendChild(roadmap);
            updateRoadmapStatus(roadmapId, columnId);
        } else {
            console.error("Roadmap Element: null");
        }
    };
});








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
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                fetch("http://52.59.213.161:8080/create_roadmap", {
                    method: "POST",
                    body: JSON.stringify(data),
                    headers: {
                        "Content-Type": "application/json",
                    },
                })
                .then(response => response.json())
                .then((data) => {
                    console.log(response.status); 
                    if (response.ok) {
                        url = 'http://5' + data
                        window.open(url, "_blank");
                    }
                })
                .catch((error) => {
                    console.error("Error:", error);
                });
            })
            .catch((error) => {
                console.error("Error:", error);
            });
        });
});