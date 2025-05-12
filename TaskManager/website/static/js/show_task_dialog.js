// modal.js - Modal form module

// Function to show modal form and return a promise with the form values
function showTaskForm(defaults = null) {
    return new Promise((resolve, reject) => {
        try {
            // Create a link element for the CSS
            const styleLink = document.createElement('link');
            styleLink.rel = 'stylesheet';
            styleLink.href = 'static/css/task_form.css';
            styleLink.id = 'modal-styles';
            document.head.appendChild(styleLink);
            // Fetch the modal HTML
            fetch('static/html/task_dialog.html')
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to load modal');
                    }
                    return response.text();
                })
                .then(html => {
                    // Create a temporary container
                    const temp = document.createElement('div');
                    temp.innerHTML = html;

                    // Append the dialog to the body
                    const dialog = temp.querySelector('dialog');
                    document.body.appendChild(dialog);

                    // Show the modal
                    const formModal = document.getElementById('formModal');
                    formModal.showModal();

                    // Populate form with default values if provided
                    if (defaults) {
                        populateFormWithDefaults(defaults);
                    }

                    // Set up event listeners
                    setupModalEventListeners(resolve, reject);
                })
                .catch(error => {
                    console.error('Error loading modal:', error);
                    reject(error);
                });
        } catch (error) {
            reject(error);
        }
    });
}

/**
 * Populates form fields with default values
 * @param {Object} defaultValues - Object containing default values for form fields
 */
function populateFormWithDefaults(defaultValues) {
    // For each possible form field, check if a default value exists and set it
    if (defaultValues.title !== undefined) {
        document.getElementById('title').value = defaultValues.title;
    }
    if (defaultValues.importance !== undefined) {
        document.getElementById('importance').value = defaultValues.importance;
    }
    if (defaultValues.deadline !== undefined) {
        document.getElementById('deadline').value = defaultValues.deadline;
    }
    if (defaultValues.est_time_days !== undefined) {
        document.getElementById('est_time_days').value = defaultValues.est_time_days;
    }
    if (defaultValues.description !== undefined) {
        document.getElementById('description').value = defaultValues.description;
    }
}


// Function to set up event listeners for the modal
function setupModalEventListeners(resolve, reject) {
    const formModal = document.getElementById('formModal');
    const modalForm = document.getElementById('modalForm');
    const cancelBtn = document.getElementById('cancelBtn');

    // Close modal when cancel button is clicked
    cancelBtn.addEventListener('click', () => {
        removeModal();
        resolve(null); // Resolve with null to indicate cancellation
    });

    // Handle form submission
    modalForm.addEventListener('submit', (event) => {
        // Collect form values
        const values = {
            title: document.getElementById('title').value,
            importance: document.getElementById('importance').value,
            deadline: document.getElementById('deadline').value,
            est_time_days: document.getElementById('est_time_days').value,
            description: document.getElementById('description').value
        };

        // Remove the modal after a short delay to allow the dialog to close properly
        setTimeout(() => {
            removeModal();
            resolve(values); // Resolve the promise with the form values
        }, 100);
    });
}

// Function to remove the modal from the DOM
function removeModal() {
    const formModal = document.getElementById('formModal');
    if (formModal) {
        formModal.close();
        formModal.remove();
    }

    // Also remove the CSS
    const modalStyles = document.getElementById('modal-styles');
    if (modalStyles) {
        modalStyles.remove();
    }
}

// Export the function to be used in other files
export { showTaskForm };