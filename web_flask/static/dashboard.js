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
        var planningTags = document.querySelectorAll('[id^="planning_"]');
        var inProgressTags = document.querySelectorAll('[id^="inProgress_"]');
        var CompletedTags = document.querySelectorAll('[id^="completed_"]');
        var count1 = planningTags.length;
        var count2 = inProgressTags.length;
        var count3 = CompletedTags.length;
        document.getElementById("planning_count").textContent = count1;
        document.getElementById("inProgress_count").textContent = count2;
        document.getElementById("completed_count").textContent = count3;
    }
    displayCount();


    // Function to handle drag events
    function drag(event) {
        event.dataTransfer.setData("text", event.target.id);
    }
    
    // Function to allow dropping elements
    function allowDrop(event) {
        event.preventDefault();
    }
    
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
    }

    $('.project-box-wrapper').on('dragstart', drag);
    $('.droppable').on('dragover', allowDrop);
    $('.droppable').on('drop', drop);
});
