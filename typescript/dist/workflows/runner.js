"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.startTaskServer = startTaskServer;
exports.run = run;
const errors_js_1 = require("./client/errors.js");
const executor_js_1 = require("./executor.js");
async function startTaskServer() {
    const mode = process.env.RENDER_SDK_MODE || 'run';
    const socketPath = process.env.RENDER_SDK_SOCKET_PATH;
    if (!socketPath) {
        throw new errors_js_1.RenderError('RENDER_SDK_SOCKET_PATH environment variable is required');
    }
    const executor = new executor_js_1.TaskExecutor(socketPath);
    if (mode === 'register') {
        await executor.registerTasks();
    }
    else if (mode === 'run') {
        await executor.executeTask();
    }
    else {
        throw new errors_js_1.RenderError(`Unknown SDK mode: ${mode}`);
    }
}
async function run(socketPath) {
    const executor = new executor_js_1.TaskExecutor(socketPath);
    await executor.executeTask();
}
