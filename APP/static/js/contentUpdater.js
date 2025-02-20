// contentUpdater.js

if (document.getElementById('annotation-form')) {
    // Function to handle form submission
    document.getElementById('annotation-form').addEventListener('submit', function(event) {
        // event.preventDefault(); // Prevent default form submission
        // Collect non-empty annotation terms and their indexes
        let formData = new FormData(); // Create a new FormData object
        // Iterate over each annotation input field
        document.querySelectorAll('.annotation-input').forEach(function(input, index) {
        // Check if the input field is not empty
            if (input.value.trim() !== '') {
                // Append the non-empty annotation term to the FormData object
                formData.append('annotations[]', input.value);
                // Get the corresponding annotation index from the hidden input field
                let indexInput = input.nextElementSibling;
                // Append the index to the FormData object
                formData.append('annotation_indexes[]', indexInput.value);
            }
        })
    });

    // Append the record ID to the FormData object
    formData.append('record_id', document.querySelector('[name="record_id"]').value);
    // Append the page number to the FormData object
    formData.append('page', document.querySelector('[name="page"]').value);
    // Submit the form with non-empty annotation terms
    fetch('/annotate', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Handle response data if needed
        console.log(data);
        // Check if the operation was successful
        if (data.success) {
            // Replace the entire content of the frame with the updated HTML content
            document.querySelector('.frame').innerHTML = data.html;
            // Optionally, refresh the table content
            // Clear input fields
            document.querySelectorAll('.annotation-input').forEach(input => {
                input.value = '';
                input.placeholder = 'Enter ' + input.name;
            });
            // Optionally, update specific parts of the page dynamically
            // For example, update the table with the latest data
            // You can make a separate fetch request to retrieve the updated data
            // and then update the table content accordingly
        } else {
            // Handle error
            console.error('An error occurred:', data.error);
        }
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}

// Function to make input resizable
Array.from( document.querySelectorAll('[data-expand]'), (input)=>{
    let parent = input.parentNode;
    function updateSize(){
        parent.dataset.value = input.value
    }
    input.addEventListener('input', updateSize);
    updateSize();
});



