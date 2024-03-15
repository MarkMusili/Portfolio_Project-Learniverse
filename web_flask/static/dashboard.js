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
            let column;
            
            // Prevent default behavior for dragover
            $(".planningColumn, .inProgressColumn, .completedColumn").on("dragover", function(e) {
                e.preventDefault();
            });
            
            // Append the selected element to the target column on drop
            $(".planningColumn").on("drop", function(e) {
                $(".planningColumn").append(selected);
                selected = null;
            });
            $(".inProgressColumn").on("drop", function(e) {
                $(".inProgressColumn").append(selected);
                selected = null;
            });
            $(".completedColumn").on("drop", function(e) {
                $(".completedColumn").append(selected);
                selected = null;
            });
        });
    }
    dragAndDrop();
    displayCount();
});
