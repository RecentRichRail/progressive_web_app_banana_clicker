document.addEventListener('DOMContentLoaded', (event) => {
    let count = 0;
    let unsentCount = 0;
    const countDisplay = document.getElementById('count');
    const clickButton = document.getElementById('clickButton');

    // Function to get initial user stats from the server
    function getInitialUserStats() {
        fetch('/apiv1/games/banana_clicker/get_user_stats', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({id: userId})
        })
        .then(response => response.json())
        .then(data => {
            // Set the count with the initial count from the server
            count = data.bananas;
            countDisplay.textContent = count;
        })
        .catch(error => console.error('Error:', error));
    }

    // Function to increment the unsent count
    function incrementUnsentCount() {
        // Increment the unsent count
        unsentCount++;

        // Optimistically update the count on the client side
        count++;
        countDisplay.textContent = count;
    }

    // Function to send the unsent count to the server
    function sendUnsentCount() {
        if (unsentCount > 0) {
            let sentCount = unsentCount;
            fetch('/apiv1/games/banana_clicker/banana_button_action_press', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({id: userId, clicks: sentCount})
            })
            .then(() => {
                // Subtract the sent count from the unsent count
                unsentCount -= sentCount;
    
                // Reset the sent count
                sentCount = 0;
            })
            .catch(error => console.error('Error:', error));
        }
    }

    // Get the initial count from the server on application load
    getInitialUserStats();

    // Send the unsent count to the server every 5 seconds
    setInterval(sendUnsentCount, 2000);

    // Increment the unsent count when the button is clicked
    clickButton.addEventListener('click', incrementUnsentCount);

    document.getElementById('clickButton').addEventListener('click', function() {
        // Create a new banana image
        var banana = document.createElement('img');
        banana.src = 'static/images/banana.png'; // Set the source to your banana image
        banana.className = 'fallingBanana'; // Apply the falling animation
        banana.style.width = '50px'; // Set the width of the banana image

        // Position the banana image higher on the screen
        banana.style.top = '-20px'; // Adjust as needed

        // Randomly position the banana image horizontally
        banana.style.left = Math.random() * document.querySelector('.main-content').offsetWidth + 'px';

        // Add the banana image to the .main-content div
        document.querySelector('.main-content').appendChild(banana);

        // Remove the banana image when the animation is done
        banana.addEventListener('animationend', function() {
            document.querySelector('.main-content').removeChild(banana);
        });
    });
});