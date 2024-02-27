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
});

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

function updateRoadmapCounts() {
    const planningCount = document.querySelectorAll('.column[status="planning"]').length;
    const inProgressCount = document.querySelectorAll('.column[status="in_progress"]').length;
    const completedCount = document.querySelectorAll('.column[status="completed"]').length;

    // Update the HTML elements displaying the counts
    document.getElementById('planning-count').innerText = planningCount;
    document.getElementById('in_progress-count').innerText = inProgressCount;
    document.getElementById('completed-count').innerText = completedCount;
}

// Call the function to update counts initially and whenever the page content changes
updateRoadmapCounts();
