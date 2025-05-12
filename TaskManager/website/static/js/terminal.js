import {showTaskForm} from "./show_task_dialog.js";

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
    addLine('<span class="help-header">Available commands:</span>', 'info');
    addLine('<span class="help-command">help</span><span class="help-description">Show this help message</span>', 'info');
    addLine('<span class="help-command">list</span><span class="help-description">List all tasks</span>', 'info');
    addLine('<span class="help-command">view &lt;id&gt;</span><span class="help-description">View a task by ID</span>', 'info');
    addLine('<span class="help-command">add</span><span class="help-description">Add a new task. This will open a form to fill data of the new task</span>', 'info');
    addLine('<span class="help-command">edit &lt;id&gt;</span><span class="help-description">Edit a task with given ID. This will open a form</span>', 'info');
    addLine('<span class="help-command">delete &lt;id&gt;</span><span class="help-description">Delete a task by ID</span>', 'info');
    addLine('<span class="help-command">clear</span><span class="help-description">Clear the terminal</span>', 'info');
    addLine('<span class="help-command">')
}

/**
 * Sends `args` as a JSON to `endpoint` via a POST request.
 * Displays the result on the terminal
 * when silent === true the function will NOT display result on the terminal
 * when return_results === true the function will return result of fetch()
 */
async function send_terminal_cmd(endpoint, args, silent=false, return_results=false) {
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(args)
        });

        const data = await response.json();

        if (!silent) {
            if (data.status === 'success') {
                addLine(data.result, 'success');
            } else {
                addLine(data.message, 'error');
            }
        }

        if (return_results) {
            return data;
        }
        return null;
    } catch (error) {
        if (!silent) {
            addLine(`Error: ${error}`, 'error');
        }

        if (return_results) {
            return {
                status: 'error',
                message: error.toString(),
                result: null
            };
        }
        return null;
    }
}

/**
 * Processes a command entered by the user
 * @param {string} command - The command string to process
 */
async function processCommand(command) {
    // Display the command in the terminal with the prompt
    output.innerHTML += `<div class="command-line"><span class="prompt">$</span> ${command}</div>`;

    // Parse the command into the base command and its arguments
    const parts = command.trim().split(' ');  // Split by spaces
    const cmd = parts[0];                     // First part is the command name
    let args = parts.slice(1).join(' ');    // Rest is joined back as arguments

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

    if (!endpoints[cmd]) {
        // If command is not recognized and not one of our locally handled commands
        addLine(`Unknown command: '${cmd}'. Type 'help' for available commands.`, 'error');
        return;
    }
    const endpoint = endpoints[cmd];

    // Prepare the args
    if (cmd === 'add')
    {
        args = await showTaskForm();
        if (args === null)
        {
            addLine("Add command cancelled. No changes made");
            return;
        }
    }
    if (cmd === 'view' || cmd === 'edit' || cmd === 'delete')
    {
        if (parts.length !== 2)
        {
            addLine(`Command ${cmd} expected exactly one parameter - task id.`);
            return;
        }
        args = {"task_id": parts[1]};

    }

    // edit has special treatment, as it sends multiple requests
    if (cmd !== 'edit') {
        send_terminal_cmd(endpoint, args);
        return;
    }
    const task_response = await send_terminal_cmd(endpoints['view'], args, true, true);
    if (task_response.status !== 'success')
    {
        addLine(`Couldn't edit: ${task_response.message}`);
        return;
    }
    const task_data = JSON.parse(task_response.result);
    args = await showTaskForm(task_data);
    console.log("args from showTaskForm()", args);
    if (args === null)
    {
        addLine("Edit command cancelled. No changes made");
        return;
    }
    args.task_id = parts[1];
    const edit_response = await send_terminal_cmd(endpoint, args, true, true);
    if (edit_response.status !== 'success')
    {
        addLine(edit_response.message);
        return;
    }
    addLine(edit_response.result);

    send_terminal_cmd(endpoints['view'], {"task_id": parts[1]}, false, false);



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