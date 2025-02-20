$(document).ready(function() {
    $('#record-form').on('submit', function(event) {
        event.preventDefault();

        let recordId = $('#record-id').val();

        $.ajax({
            url: '/get_record_info',
            type: 'POST',
            data: { record_id: recordId },
            success: function(response) {
                if (response.error) {
                    $('#num-rec-message').text(response.error);
                    $('#num-rec-annotations').text('');
                } else {
                    $('#num-rec-message').html('<b>Messages:</b><br>' + response.messages.join('<br>'));
                    $('#num-rec-annotations').html('<b>Annotations:</b><br>' + response.annotations.join('<br>'));
                }
            },
            error: function() {
                $('#num-rec-message').text('An error occurred');
                $('#num-rec-annotations').text('');
            }
        });
    });
});


/*$(document).ready(function () {
    $('#fetch-data').click(function () {
        fetchRecordDataExample();
    });

    function fetchRecordDataExample() {
        $.ajax({
            url: '/fetch_record_data', // This should be the route you set up in your Flask app
            type: 'GET',
            success: function (data) {
                // Assuming data is in JSON format and contains the necessary information
                $('#record-data').html(renderRecordData(data));
            },
            error: function (xhr, status, error) {
                console.error('Error fetching record data:', error);
            }
        });
    }

    function renderRecordData(data) {
        // Generate HTML to display the record data
        let html = '<h3>Record Data</h3>';
        data.records.forEach(record => {
            html += `<div class="record">
                        <p><strong>ID:</strong> ${record.rowid}</p>
                        <p><strong>Repository:</strong> ${record.Repository}</p>
                        <p><strong>Commit Message:</strong> ${record['Commit Message']}</p>
                        <p><strong>Filename:</strong> ${record.Filename}</p>
                        <p><strong>Code Changes:</strong> ${record['Code Changes']}</p>
                    </div>`;
        });
        return html;
    }
});

document.getElementById('record-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const recordNumber = document.getElementById('record-number').value;

    if (recordNumber) {
        fetchRecordData(recordNumber);
    } else {
        alert('Please enter a record number.');
    }
});

function fetchRecordData(recordNumber) {
    // Create an AJAX request to fetch record data
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/fetch_record_data/' + recordNumber, true);  // Adjust the URL as needed
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                // Parse the JSON response
                var response = JSON.parse(xhr.responseText);
                // Update the last-rec-content div with the new record data
                updateRecordContent(response);
            } else {
                alert('Error: ' + xhr.status);
            }
        }
    };
    xhr.send();
}

function updateRecordContent(record) {
    const lastRecMsgDiv = document.getElementById('num-rec-message');
    const lastRecAnnotationsDiv = document.getElementById('num-rec-annotations');

    lastRecMsgDiv.innerHTML = '';
    lastRecAnnotationsDiv.innerHTML = '';

    const commitInfo = record.commit_info;
    const annotationFields = record.annotation_fields;

    if (record) {
        // Update commit information
        commitInfo.forEach((info, index) => {
            const fieldDiv = document.createElement('div');
            const truncatedValue = info.length > 1000 ? info.substring(0, 1000) + '...' : info;
            fieldDiv.innerHTML = `<strong>${record.commit_info_labels[index]}:</strong> ${truncatedValue}`;
            lastRecMsgDiv.appendChild(fieldDiv);
        });

        // Update annotation fields
        annotationFields.forEach((field, index) => {
            const fieldDiv = document.createElement('div');
            const fieldValue = field;
            fieldDiv.innerHTML = `<strong>${record.annotation_fields_labels[index]}:</strong> ${fieldValue}`;

            // Create a copy button
            const copyButton = document.createElement('button');
            copyButton.textContent = 'Copy to Clip';

            // Add an onclick event listener to the button
            copyButton.onclick = function() {
                // Copy the field value to the clipboard
                const textField = document.createElement('textarea');
                textField.innerText = fieldValue;
                document.body.appendChild(textField);
                textField.select();
                document.execCommand('copy');
                document.body.removeChild(textField);

                // Provide visual feedback that the value has been copied
                copyButton.textContent = 'Copied!';
                setTimeout(() => {
                    copyButton.textContent = 'Copy to Clip';
                }, 2000); // Reset button text after 2 seconds
            };

            // Append the copy button to the fieldDiv
            fieldDiv.appendChild(copyButton);

            lastRecAnnotationsDiv.appendChild(fieldDiv);

            // Insert a horizontal blank space
            const horizontalSpace = document.createElement('div');
            horizontalSpace.style.height = '7px'; // Adjust the height as needed
            lastRecAnnotationsDiv.appendChild(horizontalSpace);
        });
    } else {
        lastRecAnnotationsDiv.innerHTML = 'No record found';
        lastRecMsgDiv.innerHTML = 'No record found';
    }
}*/

