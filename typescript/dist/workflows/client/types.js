"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.TaskRunStatus = void 0;
var TaskRunStatus;
(function (TaskRunStatus) {
    TaskRunStatus["PENDING"] = "pending";
    TaskRunStatus["RUNNING"] = "running";
    TaskRunStatus["COMPLETED"] = "completed";
    TaskRunStatus["FAILED"] = "failed";
})(TaskRunStatus || (exports.TaskRunStatus = TaskRunStatus = {}));
