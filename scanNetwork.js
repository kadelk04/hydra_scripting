const { spawn } = require('child_process');
const path = require('path');

function scanNetwork(network, username) {

    console.log(`This is the username ${username}`);

    const scriptPath = path.resolve(__dirname, 'nmap-hydra.sh');
    console.log(`Resolved script path: ${scriptPath}`);

    const args = [scriptPath, network, username];
    console.log (`These are the args ${args}`)

    const command = '/bin/bash';

    console.log(`Executing command: ${command} "${args.join('" "')}"`);

    const child = spawn('/bin/bash', args);

    // Handle stdout data
    child.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
    });

    // Handle stderr data
    child.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
    });
    
    
    // Handle errors
    child.on('error', (error) => {
    console.error(`Error: ${error.message}`);
    });

    // Handle process close
    child.on('close', (code) => {
    console.log(`Child process exited with code ${code}`);
    });
}

scanNetwork('10.10.102.19', 'bee');