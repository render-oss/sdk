"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.UDSClient = void 0;
const net = __importStar(require("node:net"));
class UDSClient {
    constructor(socketPath) {
        this.socketPath = socketPath;
    }
    async getInput() {
        return this.request('/input', 'GET');
    }
    buildCallbackBody(results, error) {
        if (results) {
            const resultsArray = [results];
            const output = Buffer.from(JSON.stringify(resultsArray)).toString('base64');
            return {
                complete: {
                    output,
                },
            };
        }
        return {
            error: {
                details: error,
            },
        };
    }
    async sendCallback(results, error) {
        await this.request('/callback', 'POST', this.buildCallbackBody(results, error));
    }
    async runSubtask(taskName, input) {
        const inputBase64 = Buffer.from(JSON.stringify(input)).toString('base64');
        const body = {
            task_name: taskName,
            input: inputBase64,
        };
        const response = await this.request('/run-subtask', 'POST', body);
        return response.task_run_id;
    }
    async getSubtaskResult(subtaskId) {
        const body = {
            task_run_id: subtaskId,
        };
        return this.request('/get-subtask-result', 'POST', body);
    }
    async registerTasks(tasks) {
        const body = {
            tasks: tasks.map((task) => ({
                name: task.name,
                options: task.options,
            })),
        };
        await this.request('/register-tasks', 'POST', body);
    }
    async request(path, method, body) {
        return new Promise((resolve, reject) => {
            const client = net.createConnection({ path: this.socketPath }, () => {
                const bodyStr = body ? JSON.stringify(body) : '';
                const request = `${method} ${path} HTTP/1.1\r\nHost: unix\r\nContent-Length: ${bodyStr.length}\r\nContent-Type: application/json\r\n\r\n${bodyStr}`;
                client.write(request);
            });
            let data = '';
            let contentLength = null;
            let headersParsed = false;
            let bodyStartIndex = -1;
            client.on('data', (chunk) => {
                data += chunk.toString();
                if (!headersParsed) {
                    const headerEndIndex = data.indexOf('\r\n\r\n');
                    if (headerEndIndex !== -1) {
                        headersParsed = true;
                        bodyStartIndex = headerEndIndex + 4;
                        const headers = data.substring(0, headerEndIndex);
                        const contentLengthMatch = headers.match(/Content-Length:\s*(\d+)/i);
                        if (contentLengthMatch) {
                            contentLength = parseInt(contentLengthMatch[1], 10);
                        }
                    }
                }
                if (headersParsed && contentLength !== null) {
                    const bodyReceived = data.length - bodyStartIndex;
                    if (bodyReceived >= contentLength) {
                        client.end();
                    }
                }
            });
            client.on('end', () => {
                try {
                    const lines = data.split('\r\n');
                    const statusLine = lines[0];
                    const statusCode = parseInt(statusLine.split(' ')[1], 10);
                    if (statusCode >= 400) {
                        reject(new Error(`HTTP ${statusCode}: ${data}`));
                        return;
                    }
                    const emptyLineIndex = lines.indexOf('');
                    if (emptyLineIndex === -1) {
                        resolve(undefined);
                        return;
                    }
                    const bodyLines = lines.slice(emptyLineIndex + 1);
                    const responseBody = bodyLines.join('\r\n').trim();
                    if (!responseBody) {
                        resolve(undefined);
                        return;
                    }
                    resolve(JSON.parse(responseBody));
                }
                catch (error) {
                    reject(error);
                }
            });
            client.on('error', (error) => {
                reject(error);
            });
        });
    }
}
exports.UDSClient = UDSClient;
