// The code below is related to population of popup
// Function to display the popup with the given message
function displayPopup(message) {
    // Set the message as the content of the popup
    document.getElementById('popup-message').innerText = message;
    // Display the overlay and popup
    document.getElementById('overlay').style.display = 'block';
}
// Function to close the popup
function closePopup() {
    // Hide the overlay and popup
    document.getElementById('overlay').style.display = 'none';
}
// Function to handle submitting the form
function handleSubmit(event) {
    // Prevent the default form submission behavior
    event.preventDefault();
    // Default text for popup
    defaultText = "Sending to OpenAI. Please wait..."
    // Display the concatenated text in the popup for 5 seconds
    displayPopup(defaultText);
    // Get the fixed line from the hidden input field
    //var fixedText = document.getElementById('fixed-text').value;
    var fixedText = "What bugs does this code change resolve? Does this solve any vulnerabilities? Is this a classical or quantum fix?: "
    // Get the text from the input field
    var inputText = document.getElementById('code-changes').value;
    // Concatenate the fixed line and the input text
    var popupText = fixedText + inputText;
    // After 5 seconds, send the text to the Flask server using AJAX
    setTimeout(function() {
        // Send the text to the Flask server using AJAX
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/generate_text', true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    // Parse the JSON response
                    var response = JSON.parse(xhr.responseText);
                 // Display the generated text in the popup
                    displayPopup(response.generated_text);
                } else {
                    alert('Error: ' + xhr.status);
                }
            }
        };
        xhr.send('code_changes_text=' + encodeURIComponent(popupText));
    }, 500);
}
// Add event listener to the form submission
document.getElementById('popup-form').addEventListener('submit', handleSubmit);
// Add event listener to close the popup when the close button is clicked
document.getElementById('close-popup').addEventListener('click', closePopup);