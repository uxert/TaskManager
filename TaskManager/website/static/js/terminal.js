const output = document.getElementById('terminal-output');  // The terminal output display area
const input = document.getElementById('command-input');     // The command input field

// Variables for command history functionality
let commandHistory = [];  // Array to store previously entered commands
let historyIndex = -1;    // Current position in command history (-1 means not browsing history)

/**
 * Adds a new line to the terminal output
 * @param {string} text - The text content to add
 * @param {string} className - Optional CSS class for styling (e.g., 'error', 'success', 'info')
 */
function addLine(text, className = '') {
    // Create a new line with the provided text and class
    output.innerHTML += `<div class="response-line ${className}">${text}</div>`;
    // Scroll to the bottom of the output to show the newest content
    output.scrollTop = output.scrollHeight;
}

/**
 * Displays formatted help text in the terminal
 */
function displayHelp() {
    // Add header
    addLine('<strong>Available commands:</strong>', 'info');
    addLine('<span class="help-command">help</span>: Show this help message', 'info');
    addLine('<span class="help-command">list</span>: List all tasks', 'info');
    addLine('<span class="help-command">view &lt;id&gt;</span>: View a task by ID', 'info');
    addLine('<span class="help-command">add &lt;title&gt; &lt;content&gt;</span>: Add a new task', 'info');
    addLine('<span class="help-command">edit &lt;id&gt; title=&lt;new_title&gt; content=&lt;new_content&gt;</span>: Edit a note', 'info');
    addLine('<span class="help-command">delete &lt;id&gt;</span>: Delete a task by ID', 'info');
    addLine('<span class="help-command">clear</span>: Clear the terminal', 'info');
    addLine('<span class="help-command">')
}

/**
 * Sends `args` as a JSON to `endpoint` via a POST request.
 * Displays the result on the terminal
 */
function send_terminal_cmd(endpoint, args) {
    // Send a request to the appropriate endpoint
    fetch(endpoint, {
        method: 'POST',                                  // Using POST method
        headers: {'Content-Type': 'application/json'},   // JSON content type
        body: JSON.stringify(args)               // Send arguments as JSON
    })
        .then(response => response.json())  // Parse JSON response
        .then(data => {
            // Handle the response based on status
            if (data.status === 'success') {
                // Display successful result with success styling
                addLine(data.result, 'success');
            } else {
                // Display error message with error styling
                addLine(data.message, 'error');
            }
        })
        .catch(error => {
            // Handle any network or other errors
            addLine(`Error: ${error}`, 'error');
        });
}

/**
 * Processes a command entered by the user
 * @param {string} command - The command string to process
 */
function processCommand(command) {
    // Display the command in the terminal with the prompt
    output.innerHTML += `<div class="command-line"><span class="prompt">$</span> ${command}</div>`;

    // Parse the command into the base command and its arguments
    const parts = command.trim().split(' ');  // Split by spaces
    const cmd = parts[0];                     // First part is the command name
    const args = parts.slice(1).join(' ');    // Rest is joined back as arguments

    if (cmd === 'clear') {
        output.innerHTML = '';
        addLine('Terminal cleared.', 'info');
        return;
    }
    if (cmd === 'help') {
        displayHelp();
        return;
    }

    // Map of command names to their corresponding server endpoints
    const endpoints = {
        'list': '/terminal/list',
        'view': '/terminal/view',
        'add': '/terminal/add',
        'edit': '/terminal/edit',
        'delete': '/terminal/delete'
    };

    // Check if the command exists in our endpoint map
    if (endpoints[cmd]) {
        const endpoint = endpoints[cmd]
        send_terminal_cmd(endpoint, args);
    } else if (cmd !== 'help' && cmd !== 'clear') {
        // If command is not recognized and not one of our locally handled commands
        addLine(`Unknown command: '${cmd}'. Type 'help' for available commands.`, 'error');
    }
}

// Set up event listener for keyboard input
input.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        // When Enter key is pressed, process the command
        const command = input.value;
        if (command.trim() !== '') {  // Only process non-empty commands
            // Add to command history at the beginning
            commandHistory.unshift(command);
            historyIndex = -1;  // Reset history index

            // Process the command
            processCommand(command);

            // Clear the input field for the next command
            input.value = '';
        }
    } else if (e.key === 'ArrowUp') {
        // Navigate command history upward (older commands)
        e.preventDefault();  // Prevent default cursor movement
        if (historyIndex < commandHistory.length - 1) {
            historyIndex++;  // Move to older command
            input.value = commandHistory[historyIndex];  // Display the command
        }
    } else if (e.key === 'ArrowDown') {
        // Navigate command history downward (newer commands)
        e.preventDefault();  // Prevent default cursor movement
        if (historyIndex > 0) {
            historyIndex--;  // Move to newer command
            input.value = commandHistory[historyIndex];  // Display the command
        } else if (historyIndex === 0) {
            // If at the newest command, clear the input
            historyIndex = -1;
            input.value = '';
        }
    }
});