export interface paths {
    '/input': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: {
            parameters: {
                query?: never;
                header?: never;
                path?: never;
                cookie?: never;
            };
            requestBody?: never;
            responses: {
                200: {
                    headers: {
                        [name: string]: unknown;
                    };
                    content: {
                        'application/json': components['schemas']['InputResponse'];
                    };
                };
                500: {
                    headers: {
                        [name: string]: unknown;
                    };
                    content?: never;
                };
            };
        };
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/callback': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post: {
            parameters: {
                query?: never;
                header?: never;
                path?: never;
                cookie?: never;
            };
            requestBody?: {
                content: {
                    'application/json': components['schemas']['CallbackRequest'];
                };
            };
            responses: {
                200: {
                    headers: {
                        [name: string]: unknown;
                    };
                    content?: never;
                };
                400: {
                    headers: {
                        [name: string]: unknown;
                    };
                    content?: never;
                };
                401: {
                    headers: {
                        [name: string]: unknown;
                    };
                    content?: never;
                };
                403: {
                    headers: {
                        [name: string]: unknown;
                    };
                    content?: never;
                };
                500: {
                    headers: {
                        [name: string]: unknown;
                    };
                    content?: never;
                };
            };
        };
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/register-tasks': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post: {
            parameters: {
                query?: never;
                header?: never;
                path?: never;
                cookie?: never;
            };
            requestBody?: {
                content: {
                    'application/json': components['schemas']['Tasks'];
                };
            };
            responses: {
                200: {
                    headers: {
                        [name: string]: unknown;
                    };
                    content?: never;
                };
                400: {
                    headers: {
                        [name: string]: unknown;
                    };
                    content?: never;
                };
                500: {
                    headers: {
                        [name: string]: unknown;
                    };
                    content?: never;
                };
            };
        };
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/run-subtask': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post: {
            parameters: {
                query?: never;
                header?: never;
                path?: never;
                cookie?: never;
            };
            requestBody?: {
                content: {
                    'application/json': components['schemas']['RunSubtaskRequest'];
                };
            };
            responses: {
                200: {
                    headers: {
                        [name: string]: unknown;
                    };
                    content: {
                        'application/json': components['schemas']['RunSubtaskResponse'];
                    };
                };
                500: {
                    headers: {
                        [name: string]: unknown;
                    };
                    content?: never;
                };
            };
        };
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/get-subtask-result': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post: {
            parameters: {
                query?: never;
                header?: never;
                path?: never;
                cookie?: never;
            };
            requestBody?: {
                content: {
                    'application/json': components['schemas']['SubtaskResultRequest'];
                };
            };
            responses: {
                200: {
                    headers: {
                        [name: string]: unknown;
                    };
                    content: {
                        'application/json': components['schemas']['SubtaskResultResponse'];
                    };
                };
                500: {
                    headers: {
                        [name: string]: unknown;
                    };
                    content?: never;
                };
            };
        };
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
}
export type webhooks = Record<string, never>;
export interface components {
    schemas: {
        CallbackRequest: {
            error?: components['schemas']['TaskError'];
            complete?: components['schemas']['TaskComplete'];
        };
        TaskError: {
            details: string;
            stack_trace?: string;
        };
        TaskComplete: {
            output: string;
        };
        RunSubtaskRequest: {
            task_name: string;
            input?: string;
        };
        RunSubtaskResponse: {
            task_run_id: string;
        };
        SubtaskResultRequest: {
            task_run_id: string;
        };
        SubtaskResultResponse: {
            still_running: boolean;
            error?: components['schemas']['TaskError'];
            complete?: components['schemas']['TaskComplete'];
        };
        InputResponse: {
            task_name: string;
            input: string;
        };
        Tasks: {
            tasks: components['schemas']['Task'][];
        };
        Task: {
            name: string;
            options?: components['schemas']['TaskOptions'];
        };
        TaskOptions: {
            retry?: components['schemas']['RetryConfig'];
        };
        RetryConfig: {
            max_retries?: number;
            wait_duration_ms?: number;
            factor?: number;
        };
    };
    responses: never;
    parameters: never;
    requestBodies: never;
    headers: never;
    pathItems: never;
}
export type $defs = Record<string, never>;
export type operations = Record<string, never>;
//# sourceMappingURL=schema.d.ts.map