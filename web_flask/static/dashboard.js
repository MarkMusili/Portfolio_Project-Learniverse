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
        if (imgElement.src.endsWith('slider-dark-mode-right.png')) {
            imgElement.src = '../static/Images/slider-dark-mode-left.png';
        } else {
            imgElement.src = '../static/Images/slider-dark-mode-right.png';
        }
    });

    // Function to count the elements in one column
    function displayCount() {
        // Store each of the elements in variables
        var planningTags = document.querySelectorAll('[id^="planning_"]');
        var inProgressTags = document.querySelectorAll('[id^="inProgress_"]');
        var completedTags = document.querySelectorAll('[id^="completed_"]');

        // Count each of the columns
        var count1 = planningTags.length;
        var count2 = inProgressTags.length;
        var count3 = completedTags.length;

        // Display the final count of each column
        document.getElementById("planningCount").textContent = count1;
        document.getElementById("in_progressCount").textContent = count2;
        document.getElementById("completedCount").textContent = count3;
    }
    displayCount();


    // Function to handle drag events
    function dragAndDrop() {
        // Implement Drag and Drop feature for each map
        $(".planning, .in_progress, .completed").on("dragstart", function(e) {
            let selected = $(this);
            r_id = selected.attr('id').split('_')[1];

            // Prevent default behavior for dragover
            $(".planningColumn, .inProgressColumn, .completedColumn").on("dragover", function(e) {
                e.preventDefault();
            });
            
            // Append the selected element to the target column on drop
            $(".planningColumn").on("drop", function(e) {
                selected.attr('id', 'planning_' + r_id);
                selected.removeClass('planning in_progress completed').addClass('planning');
                $(".planningColumn").append(selected);
                selected = null;
            });

            $(".inProgressColumn").on("drop", function(e) {
                selected.attr('id', 'inProgress_' + r_id);
                selected.removeClass('planning in_progress completed').addClass('in_progress');
                $(".inProgressColumn").append(selected);
                selected = null;
            });

            $(".completedColumn").on("drop", function(e) {
                selected.attr('id', 'completed_' + r_id);
                selected.removeClass('planning in_progress completed').addClass('completed');
                $(".completedColumn").append(selected);
                selected = null;
            });
        });
    }
    dragAndDrop();
    displayCount();
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