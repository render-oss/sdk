"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getCurrentContext = getCurrentContext;
exports.setCurrentContext = setCurrentContext;
exports.task = task;
const node_async_hooks_1 = require("node:async_hooks");
const registry_js_1 = require("./registry.js");
const taskContextStorage = new node_async_hooks_1.AsyncLocalStorage();
function getCurrentContext() {
    return taskContextStorage.getStore();
}
function setCurrentContext(context, fn) {
    return taskContextStorage.run(context, fn);
}
function task(options, func) {
    const registry = registry_js_1.TaskRegistry.getInstance();
    registry.register(func, options);
    return ((...args) => {
        const context = getCurrentContext();
        if (!context) {
            return func(...args);
        }
        const result = context.executeTask(func, options.name, ...args);
        return result.get();
    });
}
