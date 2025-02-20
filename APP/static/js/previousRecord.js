// Block of code to invoke the Previous Record, that fetches the datarows from the database

// Function to show previous record annotation
function showPreviousRecordAnnotation() {
    const previousRecord = {{ previous_record|tojson }};
    const lastRecMsgDiv = document.getElementById('last-rec-message');
    lastRecMsgDiv.innerHTML = '';
    const lastRecAnnotationsDiv = document.getElementById('last-rec-annotations');
    lastRecAnnotationsDiv.innerHTML = '';
    const annotationFields = {{ annotation_fields_display|tojson }};
    const commitInfo = {{ commit_info|tojson }};
    if (previousRecord) {
        for (let i = 0; i < commitInfo.length; i++) {
            const fieldDiv = document.createElement('div');
            const messageToRemove = "Analyze this manually, DO NOT USE \'ANALYZE\' button (Above OpenAI token limit) - ****************************************************************"
            const fieldValue = previousRecord[i + 1];
            const updatedFieldValue = fieldValue.replace(messageToRemove, '');
            const truncatedValue = updatedFieldValue.length > 1000 ? updatedFieldValue.substring(0, 1000) + '...' : updatedFieldValue;
            // fieldDiv.innerHTML = `<strong>${commitInfo[i]}:</strong> ${truncatedValue} `;
            fieldDiv.innerHTML = commitInfo[i] === 'Code Changes'
                ? `<strong>${commitInfo[i]}:</strong> <pre style="display: inline; white-space: pre-wrap; word-wrap: break-word;">${truncatedValue}</pre>`
                : `<strong>${commitInfo[i]}:</strong> ${truncatedValue}`;
            lastRecMsgDiv.appendChild(fieldDiv);
            lastRecMsgDiv.appendChild(document.createElement('br'));
        }
        for (let i = 0; i < annotationFields.length; i++) {
            const fieldDiv = document.createElement('div');
            const fieldValue = previousRecord[i + 5];
            fieldDiv.innerHTML = `<strong>${annotationFields[i]}:</strong> ${previousRecord[i + 5]}`;
            // Create a button element
            const copyButton = document.createElement('button');
            copyButton.textContent = 'Copy to Clip';
            // Add an onclick event listener to the button
            copyButton.onclick = function() {
                // Copy the field value to the clipboard
                const textField = document.createElement('textarea');
                textField.innerText = fieldValue; // Use fieldValue instead of updatedFieldValue
                document.body.appendChild(textField);
                textField.select();
                document.execCommand('copy');
                textField.remove();
                // Provide visual feedback that the value has been copied
                copyButton.textContent = 'Copied!';
                setTimeout(() => {
                    copyButton.textContent = 'Copy to Clip';
                }, 2000); // Reset button text after 2 seconds
            };
            // Create a non-breaking space to add space before the button
            const space = document.createElement('span');
            space.innerHTML = '&nbsp;';
            // Append the space and then the copy button to the fieldDiv
            fDiv.appendChild(space);
            // Append the copy button to the fieldDiv
            fieldDiv.appendChild(copyButton);
            lastRecAnnotationsDiv.appendChild(fieldDiv);
            // Insert a horizontal blank space
            const horizontalSpace = document.createElement('div');
            horizontalSpace.style.height = '7px'; // Adjust the height as needed
            lastRecAnnotationsDiv.appendChild(horizontalSpace);
        }
    } else {
        lastRecAnnotationsDiv.innerHTML = 'No previous record';
        lastRecMsgDiv.innerHTML = 'No previous record';
    }
}
// Call the function to show previous record annotation on page load
window.onload = function() {
    showPreviousRecordAnnotation();
};
