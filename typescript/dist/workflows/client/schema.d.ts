export interface paths {
    '/blueprints': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['list-blueprints'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/blueprints/{blueprintId}': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                blueprintId: components['parameters']['blueprintId'];
            };
            cookie?: never;
        };
        get: operations['retrieve-blueprint'];
        put?: never;
        post?: never;
        delete: operations['disconnect-blueprint'];
        options?: never;
        head?: never;
        patch: operations['update-blueprint'];
        trace?: never;
    };
    '/blueprints/{blueprintId}/syncs': {
        parameters: {
            query?: {
                cursor?: components['parameters']['cursorParam'];
                limit?: components['parameters']['limitParam'];
            };
            header?: never;
            path: {
                blueprintId: components['parameters']['blueprintId'];
            };
            cookie?: never;
        };
        get: operations['list-blueprint-syncs'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/disks': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['list-disks'];
        put?: never;
        post: operations['add-disk'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/disks/{diskId}': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                diskId: components['parameters']['diskId'];
            };
            cookie?: never;
        };
        get: operations['retrieve-disk'];
        put?: never;
        post?: never;
        delete: operations['delete-disk'];
        options?: never;
        head?: never;
        patch: operations['update-disk'];
        trace?: never;
    };
    '/disks/{diskId}/snapshots': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                diskId: string;
            };
            cookie?: never;
        };
        get: operations['list-snapshots'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/disks/{diskId}/snapshots/restore': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                diskId: string;
            };
            cookie?: never;
        };
        get?: never;
        put?: never;
        post: operations['restore-snapshot'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/users': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['get-user'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/owners': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['list-owners'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/owners/{ownerId}': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                ownerId: string;
            };
            cookie?: never;
        };
        get: operations['retrieve-owner'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/owners/{ownerId}/members': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                ownerId: string;
            };
            cookie?: never;
        };
        get: operations['retrieve-owner-members'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/owners/{ownerId}/audit-logs': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                ownerId: components['parameters']['ownerIdPathParam'];
            };
            cookie?: never;
        };
        get: operations['list-owner-audit-logs'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/organizations/{orgId}/audit-logs': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                orgId: string;
            };
            cookie?: never;
        };
        get: operations['list-organization-audit-logs'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/notification-settings/owners/{ownerId}': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                ownerId: components['parameters']['ownerIdPathParam'];
            };
            cookie?: never;
        };
        get: operations['retrieve-owner-notification-settings'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch: operations['patch-owner-notification-settings'];
        trace?: never;
    };
    '/notification-settings/overrides': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['list-notification-overrides'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/notification-settings/overrides/services/{serviceId}': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        get: operations['retrieve-service-notification-overrides'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch: operations['patch-service-notification-overrides'];
        trace?: never;
    };
    '/registrycredentials': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['list-registry-credentials'];
        put?: never;
        post: operations['create-registry-credential'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/registrycredentials/{registryCredentialId}': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                registryCredentialId: string;
            };
            cookie?: never;
        };
        get: operations['retrieve-registry-credential'];
        put?: never;
        post?: never;
        delete: operations['delete-registry-credential'];
        options?: never;
        head?: never;
        patch: operations['update-registry-credential'];
        trace?: never;
    };
    '/services': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['list-services'];
        put?: never;
        post: operations['create-service'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/services/{serviceId}': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        get: operations['retrieve-service'];
        put?: never;
        post?: never;
        delete: operations['delete-service'];
        options?: never;
        head?: never;
        patch: operations['update-service'];
        trace?: never;
    };
    '/services/{serviceId}/cache/purge': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        get?: never;
        put?: never;
        post: operations['purge-cache'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/services/{serviceId}/deploys': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        get: operations['list-deploys'];
        put?: never;
        post: operations['create-deploy'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/services/{serviceId}/deploys/{deployId}': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
                deployId: components['parameters']['deployIdParam'];
            };
            cookie?: never;
        };
        get: operations['retrieve-deploy'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/services/{serviceId}/deploys/{deployId}/cancel': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
                deployId: components['parameters']['deployIdParam'];
            };
            cookie?: never;
        };
        get?: never;
        put?: never;
        post: operations['cancel-deploy'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/services/{serviceId}/rollback': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        get?: never;
        put?: never;
        post: operations['rollback-deploy'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/services/{serviceId}/env-vars': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        get: operations['get-env-vars-for-service'];
        put: operations['update-env-vars-for-service'];
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/services/{serviceId}/env-vars/{envVarKey}': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
                envVarKey: components['parameters']['envVarKeyParam'];
            };
            cookie?: never;
        };
        get: operations['retrieve-env-var'];
        put: operations['update-env-var'];
        post?: never;
        delete: operations['delete-env-var'];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/services/{serviceId}/secret-files': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        get: operations['list-secret-files-for-service'];
        put: operations['update-secret-files-for-service'];
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/services/{serviceId}/secret-files/{secretFileName}': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
                secretFileName: string;
            };
            cookie?: never;
        };
        get: operations['retrieve-secret-file'];
        put: operations['add-or-update-secret-file'];
        post?: never;
        delete: operations['delete-secret-file'];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/services/{serviceId}/events': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['list-events'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/services/{serviceId}/headers': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        get: operations['list-headers'];
        put: operations['update-headers'];
        post: operations['add-headers'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/services/{serviceId}/headers/{headerId}': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
                headerId: string;
            };
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        delete: operations['delete-header'];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/services/{serviceId}/routes': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        get: operations['list-routes'];
        put: operations['put-routes'];
        post: operations['add-route'];
        delete?: never;
        options?: never;
        head?: never;
        patch: operations['patch-route'];
        trace?: never;
    };
    '/services/{serviceId}/routes/{routeId}': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
                routeId: string;
            };
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        delete: operations['delete-route'];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/services/{serviceId}/custom-domains': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        get: operations['list-custom-domains'];
        put?: never;
        post: operations['create-custom-domain'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/services/{serviceId}/custom-domains/{customDomainIdOrName}': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
                customDomainIdOrName: components['parameters']['customDomainIdOrNameParam'];
            };
            cookie?: never;
        };
        get: operations['retrieve-custom-domain'];
        put?: never;
        post?: never;
        delete: operations['delete-custom-domain'];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/services/{serviceId}/custom-domains/{customDomainIdOrName}/verify': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
                customDomainIdOrName: components['parameters']['customDomainIdOrNameParam'];
            };
            cookie?: never;
        };
        get?: never;
        put?: never;
        post: operations['refresh-custom-domain'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/services/{serviceId}/suspend': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        get?: never;
        put?: never;
        post: operations['suspend-service'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/services/{serviceId}/resume': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        get?: never;
        put?: never;
        post: operations['resume-service'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/services/{serviceId}/restart': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        get?: never;
        put?: never;
        post: operations['restart-service'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/services/{serviceId}/scale': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        get?: never;
        put?: never;
        post: operations['scale-service'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/services/{serviceId}/autoscaling': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        get?: never;
        put: operations['autoscale-service'];
        post?: never;
        delete: operations['delete-autoscaling-config'];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/services/{serviceId}/preview': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        get?: never;
        put?: never;
        post: operations['preview-service'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/services/{serviceId}/jobs': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        get: operations['list-job'];
        put?: never;
        post: operations['post-job'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/services/{serviceId}/jobs/{jobId}': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
                jobId: components['parameters']['jobId'];
            };
            cookie?: never;
        };
        get: operations['retrieve-job'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/services/{serviceId}/jobs/{jobId}/cancel': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
                jobId: components['parameters']['jobId'];
            };
            cookie?: never;
        };
        get?: never;
        put?: never;
        post: operations['cancel-job'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/services/{serviceId}/instances': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        get: operations['list-instances'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/cron-jobs/{cronJobId}/runs': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                cronJobId: components['parameters']['cronJobIdParam'];
            };
            cookie?: never;
        };
        get?: never;
        put?: never;
        post: operations['run-cron-job'];
        delete: operations['cancel-cron-job-run'];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/events/{eventId}': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                eventId: components['schemas']['eventId'];
            };
            cookie?: never;
        };
        get: operations['retrieve-event'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/logs': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['list-logs'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/logs/subscribe': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['subscribe-logs'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/logs/values': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['list-logs-values'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/logs/streams/owner/{ownerId}': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['get-owner-log-stream'];
        put: operations['update-owner-log-stream'];
        post?: never;
        delete: operations['delete-owner-log-stream'];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/logs/streams/resource': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['list-resource-log-streams'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/logs/streams/resource/{resourceId}': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['get-resource-log-stream'];
        put: operations['update-resource-log-stream'];
        post?: never;
        delete: operations['delete-resource-log-stream'];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/metrics-stream/{ownerId}': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                ownerId: string;
            };
            cookie?: never;
        };
        get: operations['getOwnerMetricsStream'];
        put: operations['upsertOwnerMetricsStream'];
        post?: never;
        delete: operations['deleteOwnerMetricsStream'];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/metrics/cpu': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resolutionSeconds?: components['parameters']['resolutionParam'];
                resource?: components['parameters']['resourceQueryParam'];
                service?: components['parameters']['serviceQueryParam'];
                instance?: components['parameters']['instanceQueryParam'];
                aggregationMethod?: components['parameters']['applicationMetricAggregationMethod'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['get-cpu'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/metrics/cpu-limit': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resolutionSeconds?: components['parameters']['resolutionParam'];
                resource?: components['parameters']['resourceQueryParam'];
                service?: components['parameters']['serviceQueryParam'];
                instance?: components['parameters']['instanceQueryParam'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['get-cpu-limit'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/metrics/cpu-target': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resolutionSeconds?: components['parameters']['resolutionParam'];
                resource?: components['parameters']['resourceQueryParam'];
                service?: components['parameters']['serviceQueryParam'];
                instance?: components['parameters']['instanceQueryParam'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['get-cpu-target'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/metrics/memory': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resolutionSeconds?: components['parameters']['resolutionParam'];
                resource?: components['parameters']['resourceQueryParam'];
                service?: components['parameters']['serviceQueryParam'];
                instance?: components['parameters']['instanceQueryParam'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['get-memory'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/metrics/memory-limit': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resolutionSeconds?: components['parameters']['resolutionParam'];
                resource?: components['parameters']['resourceQueryParam'];
                service?: components['parameters']['serviceQueryParam'];
                instance?: components['parameters']['instanceQueryParam'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['get-memory-limit'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/metrics/memory-target': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resolutionSeconds?: components['parameters']['resolutionParam'];
                resource?: components['parameters']['resourceQueryParam'];
                service?: components['parameters']['serviceQueryParam'];
                instance?: components['parameters']['instanceQueryParam'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['get-memory-target'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/metrics/http-requests': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resolutionSeconds?: components['parameters']['resolutionParam'];
                resource?: components['parameters']['serviceResourceQueryParam'];
                service?: components['parameters']['serviceQueryParam'];
                host?: components['parameters']['hostQueryParam'];
                path?: components['parameters']['pathQueryParam'];
                aggregateBy?: components['parameters']['httpAggregateBy'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['get-http-requests'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/metrics/http-latency': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resolutionSeconds?: components['parameters']['resolutionParam'];
                resource?: components['parameters']['serviceResourceQueryParam'];
                service?: components['parameters']['serviceQueryParam'];
                host?: components['parameters']['hostQueryParam'];
                path?: components['parameters']['pathQueryParam'];
                quantile?: components['parameters']['quantile'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['get-http-latency'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/metrics/bandwidth': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resource?: components['parameters']['serviceResourceQueryParam'];
                service?: components['parameters']['serviceQueryParam'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['get-bandwidth'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/metrics/bandwidth-sources': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resource?: components['parameters']['serviceResourceQueryParam'];
                service?: components['parameters']['serviceQueryParam'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['get-bandwidth-sources'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/metrics/disk-usage': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resolutionSeconds?: components['parameters']['resolutionParam'];
                resource?: components['parameters']['resourceQueryParam'];
                service?: components['parameters']['serviceQueryParam'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['get-disk-usage'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/metrics/disk-capacity': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resolutionSeconds?: components['parameters']['resolutionParam'];
                resource?: components['parameters']['resourceQueryParam'];
                service?: components['parameters']['serviceQueryParam'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['get-disk-capacity'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/metrics/instance-count': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resolutionSeconds?: components['parameters']['resolutionParam'];
                resource?: components['parameters']['resourceQueryParam'];
                service?: components['parameters']['serviceQueryParam'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['get-instance-count'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/metrics/active-connections': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resolutionSeconds?: components['parameters']['resolutionParam'];
                resource?: components['parameters']['datastoreResourceQueryParam'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['get-active-connections'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/metrics/replication-lag': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resolutionSeconds?: components['parameters']['resolutionParam'];
                resource?: components['parameters']['postgresResourceQueryParam'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['get-replication-lag'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/metrics/filters/application': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resolutionSeconds?: components['parameters']['resolutionParam'];
                resource?: components['parameters']['serviceResourceQueryParam'];
                service?: components['parameters']['serviceQueryParam'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['list-application-filter-values'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/metrics/filters/http': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resolutionSeconds?: components['parameters']['resolutionParam'];
                resource?: components['parameters']['serviceResourceQueryParam'];
                service?: components['parameters']['serviceQueryParam'];
                host?: components['parameters']['hostQueryParam'];
                statusCode?: components['parameters']['httpStatusCode'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['list-http-filter-values'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/metrics/filters/path': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resolutionSeconds?: components['parameters']['resolutionParam'];
                resource?: components['parameters']['serviceResourceQueryParam'];
                service?: components['parameters']['serviceQueryParam'];
                host?: components['parameters']['hostQueryParam'];
                statusCode?: components['parameters']['httpStatusCode'];
                path?: components['parameters']['pathQueryParam'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['list-path-filter-values'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/key-value': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['list-key-value'];
        put?: never;
        post: operations['create-key-value'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/key-value/{keyValueId}': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['retrieve-key-value'];
        put?: never;
        post?: never;
        delete: operations['delete-key-value'];
        options?: never;
        head?: never;
        patch: operations['update-key-value'];
        trace?: never;
    };
    '/key-value/{keyValueId}/connection-info': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['retrieve-key-value-connection-info'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/redis': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['list-redis'];
        put?: never;
        post: operations['create-redis'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/redis/{redisId}': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['retrieve-redis'];
        put?: never;
        post?: never;
        delete: operations['delete-redis'];
        options?: never;
        head?: never;
        patch: operations['update-redis'];
        trace?: never;
    };
    '/redis/{redisId}/connection-info': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['retrieve-redis-connection-info'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/postgres': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['list-postgres'];
        put?: never;
        post: operations['create-postgres'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/postgres/{postgresId}': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['retrieve-postgres'];
        put?: never;
        post?: never;
        delete: operations['delete-postgres'];
        options?: never;
        head?: never;
        patch: operations['update-postgres'];
        trace?: never;
    };
    '/postgres/{postgresId}/connection-info': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['retrieve-postgres-connection-info'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/postgres/{postgresId}/recovery': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['retrieve-postgres-recovery-info'];
        put?: never;
        post: operations['recover-postgres'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/postgres/{postgresId}/suspend': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                postgresId: string;
            };
            cookie?: never;
        };
        get?: never;
        put?: never;
        post: operations['suspend-postgres'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/postgres/{postgresId}/resume': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                postgresId: string;
            };
            cookie?: never;
        };
        get?: never;
        put?: never;
        post: operations['resume-postgres'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/postgres/{postgresId}/restart': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                postgresId: string;
            };
            cookie?: never;
        };
        get?: never;
        put?: never;
        post: operations['restart-postgres'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/postgres/{postgresId}/failover': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                postgresId: string;
            };
            cookie?: never;
        };
        get?: never;
        put?: never;
        post: operations['failover-postgres'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/postgres/{postgresId}/export': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                postgresId: string;
            };
            cookie?: never;
        };
        get: operations['list-postgres-export'];
        put?: never;
        post: operations['create-postgres-export'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/projects': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['list-projects'];
        put?: never;
        post: operations['create-project'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/projects/{projectId}': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['retrieve-project'];
        put?: never;
        post?: never;
        delete: operations['delete-project'];
        options?: never;
        head?: never;
        patch: operations['update-project'];
        trace?: never;
    };
    '/environments': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['list-environments'];
        put?: never;
        post: operations['create-environment'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/environments/{environmentId}': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['retrieve-environment'];
        put?: never;
        post?: never;
        delete: operations['delete-environment'];
        options?: never;
        head?: never;
        patch: operations['update-environment'];
        trace?: never;
    };
    '/environments/{environmentId}/resources': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post: operations['add-resources-to-environment'];
        delete: operations['remove-resources-from-environment'];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/env-groups': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['list-env-groups'];
        put?: never;
        post: operations['create-env-group'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/env-groups/{envGroupId}': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['retrieve-env-group'];
        put?: never;
        post?: never;
        delete: operations['delete-env-group'];
        options?: never;
        head?: never;
        patch: operations['update-env-group'];
        trace?: never;
    };
    '/env-groups/{envGroupId}/services/{serviceId}': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post: operations['link-service-to-env-group'];
        delete: operations['unlink-service-from-env-group'];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/env-groups/{envGroupId}/env-vars/{envVarKey}': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['retrieve-env-group-env-var'];
        put: operations['update-env-group-env-var'];
        post?: never;
        delete: operations['delete-env-group-env-var'];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/env-groups/{envGroupId}/secret-files/{secretFileName}': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['retrieve-env-group-secret-file'];
        put: operations['update-env-group-secret-file'];
        post?: never;
        delete: operations['delete-env-group-secret-file'];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/maintenance': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['list-maintenance'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/maintenance/{maintenanceRunParam}': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['retrieve-maintenance'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch: operations['update-maintenance'];
        trace?: never;
    };
    '/maintenance/{maintenanceRunParam}/trigger': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post: operations['trigger-maintenance'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/webhooks': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['list-webhooks'];
        put?: never;
        post: operations['create-webhook'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/webhooks/{webhookId}': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                webhookId: components['parameters']['webhookIdParam'];
            };
            cookie?: never;
        };
        get: operations['retrieve-webhook'];
        put?: never;
        post?: never;
        delete: operations['delete-webhook'];
        options?: never;
        head?: never;
        patch: operations['update-webhook'];
        trace?: never;
    };
    '/webhooks/{webhookId}/events': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                webhookId: components['parameters']['webhookIdParam'];
            };
            cookie?: never;
        };
        get: operations['list-webhook-events'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/workflows': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['listWorkflows'];
        put?: never;
        post: operations['createWorkflow'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/workflows/{workflowId}': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                workflowId: components['parameters']['WorkflowIDParam'];
            };
            cookie?: never;
        };
        get: operations['getWorkflow'];
        put?: never;
        post?: never;
        delete: operations['deleteWorkflow'];
        options?: never;
        head?: never;
        patch: operations['updateWorkflow'];
        trace?: never;
    };
    '/workflowversions': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['listWorkflowVersions'];
        put?: never;
        post: operations['createWorkflowVersion'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/workflowversions/{workflowVersionId}': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                workflowVersionId: components['parameters']['WorkflowVersionIDParam'];
            };
            cookie?: never;
        };
        get: operations['getWorkflowVersion'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/tasks': {
        parameters: {
            query?: {
                ownerId?: components['parameters']['ownerIdParam'];
                taskId?: components['parameters']['TaskIdFilterParam'];
                workflowVersionId?: components['parameters']['WorkflowVersionIDFilterParam'];
                workflowId?: components['parameters']['WorkflowIDFilterParam'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['listTasks'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/tasks/{taskId}': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                taskId: components['parameters']['TaskIDParam'];
            };
            cookie?: never;
        };
        get: operations['getTask'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/task-runs': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['listTaskRuns'];
        put?: never;
        post: operations['createTask'];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/task-runs/events': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get: operations['streamTaskRunsEvents'];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    '/task-runs/{taskRunId}': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                taskRunId: components['parameters']['TaskRunIDParam'];
            };
            cookie?: never;
        };
        get: operations['getTaskRun'];
        put?: never;
        post?: never;
        delete: operations['cancelTaskRun'];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
}
export type webhooks = Record<string, never>;
export interface components {
    schemas: {
        cursor: string;
        auditLogWithCursor: {
            cursor: components['schemas']['cursor'];
            auditLog: components['schemas']['auditLog'];
        };
        auditLog: {
            id: string;
            timestamp: string;
            event: 'AcceptOrgInviteEvent' | 'AcceptTeamInviteEvent' | 'AddOrgMemberEvent' | 'ApplyBlueprintEvent' | 'ChangeEnvironmentProtectionEvent' | 'ChangeOrg2FAEnforcementEvent' | 'ChangeOrgAllowedLoginMethodsEvent' | 'ChangeOrgRoleEvent' | 'ChangeTeam2FAEnforcementEvent' | 'ChangeTeamAllowedLoginMethodsEvent' | 'ChangeTeamMemberRoleEvent' | 'ChangeWorkspaceDeployHandlingEvent' | 'ChangeWorkspacePrivacyEvent' | 'CreateCronJobEvent' | 'CreateEnvVarsEvent' | 'CreateEnvironmentEvent' | 'CreateOrgDomainEvent' | 'CreateOtelIntegrationEvent' | 'CreatePostgresEvent' | 'CreatePrivateLinkEvent' | 'CreateProjectEvent' | 'CreateRedisEvent' | 'CreateSSOConnectionEvent' | 'CreateServerDiskEvent' | 'CreateServerEvent' | 'CreateWebhookEvent' | 'CreateWorkspaceEvent' | 'DeleteCronJobEvent' | 'DeleteEnvGroupEvent' | 'DeleteEnvVarsEvent' | 'DeleteEnvironmentEvent' | 'DeleteOrgDomainEvent' | 'DeleteOtelIntegrationEvent' | 'DeletePostgresEvent' | 'DeletePrivateLinkEvent' | 'DeleteProjectEvent' | 'DeleteRedisEvent' | 'DeleteSSOConnectionEvent' | 'DeleteServerDiskEvent' | 'DeleteServerEvent' | 'DeleteWebhookEvent' | 'DeleteWorkspaceEvent' | 'DocumentDownloadEvent' | 'DownloadDatabaseBackupEvent' | 'EnableRedisInternalAuthEvent' | 'InviteToOrgEvent' | 'InviteToTeamEvent' | 'JoinTeamEvent' | 'LoginEvent' | 'LogoutEvent' | 'MaintenanceModeEnabledEvent' | 'MaintenanceModeURIUpdatedEvent' | 'MoveEnvironmentResourceEvent' | 'ProvisionOrganizationSCIMToken' | 'RemoveOrgMemberEvent' | 'RemoveUserFromTeamEvent' | 'RestoreDiskSnapshotEvent' | 'ResumePostgresEvent' | 'ResumeServiceEvent' | 'RevokeOrganizationSCIMToken' | 'SignNDAEvent' | 'StartShellEvent' | 'SuspendPostgresEvent' | 'SuspendServiceEvent' | 'UpdateEnvVarsEvent' | 'UpdateIPAllowListEvent' | 'UpdateOtelIntegrationEvent' | 'UpdateSSOConnectionEvent' | 'UpdateServiceNameEvent' | 'UpdateWebhookEvent' | 'VerifyOrgDomainEvent' | 'ViewConnectionInfoEvent' | 'ViewEnvVarValuesEvent';
            status: 'success' | 'error';
            actor: components['schemas']['auditLogActor'];
            metadata: {
                [key: string]: string;
            };
        };
        auditLogActor: {
            type: 'user' | 'rest_api' | 'system';
            email?: string;
            id?: string;
        };
        service: {
            id: string;
            autoDeploy: components['schemas']['autoDeploy'];
            autoDeployTrigger?: components['schemas']['autoDeployTrigger'];
            branch?: string;
            buildFilter?: components['schemas']['buildFilter'];
            createdAt: string;
            dashboardUrl: string;
            environmentId?: string;
            imagePath?: string;
            name: string;
            notifyOnFail: components['schemas']['notifySetting'];
            ownerId: string;
            registryCredential?: components['schemas']['registryCredentialSummary'];
            repo?: string;
            rootDir: string;
            slug: string;
            suspended: 'suspended' | 'not_suspended';
            suspenders: components['schemas']['suspenderType'][];
            type: components['schemas']['serviceType'];
            updatedAt: string;
            serviceDetails: components['schemas']['staticSiteDetails'] | components['schemas']['webServiceDetails'] | components['schemas']['privateServiceDetails'] | components['schemas']['backgroundWorkerDetails'] | components['schemas']['cronJobDetails'];
        };
        deployList: components['schemas']['deployWithCursor'][];
        workflowVersionWithCursor: {
            workflowVersion: components['schemas']['WorkflowVersion'];
            cursor: components['schemas']['cursor'];
        };
        workflowWithCursor: {
            workflow: components['schemas']['Workflow'];
            cursor: components['schemas']['cursor'];
        };
        taskWithCursor: {
            task: components['schemas']['Task'];
            cursor: components['schemas']['cursor'];
        };
        deployWithCursor: {
            deploy?: components['schemas']['deploy'];
            cursor?: components['schemas']['cursor'];
        };
        serviceAndDeploy: {
            service?: components['schemas']['service'];
            deployId?: string;
        };
        autoDeploy: 'yes' | 'no';
        autoDeployTrigger: 'commit' | 'off' | 'checksPass';
        buildFilter: {
            paths: string[];
            ignoredPaths: string[];
        };
        registryCredentialSummary: {
            id: string;
            name: string;
        };
        registryCredentialRegistry: 'GITHUB' | 'GITLAB' | 'DOCKER' | 'GOOGLE_ARTIFACT' | 'AWS_ECR';
        registryCredential: {
            id: string;
            name: string;
            registry: components['schemas']['registryCredentialRegistry'];
            username: string;
            updatedAt: string;
        };
        image: {
            ownerId: string;
            registryCredentialId?: string;
            imagePath: string;
        };
        dockerDetails: {
            dockerCommand: string;
            dockerContext: string;
            dockerfilePath: string;
            preDeployCommand?: string;
            registryCredential?: components['schemas']['registryCredential'];
        };
        nativeEnvironmentDetails: {
            buildCommand: string;
            startCommand: string;
            preDeployCommand?: string;
        };
        staticSiteDetails: {
            buildCommand: string;
            ipAllowList?: components['schemas']['cidrBlockAndDescription'][];
            parentServer?: components['schemas']['resource'];
            publishPath: string;
            pullRequestPreviewsEnabled?: components['schemas']['pullRequestPreviewsEnabled'];
            previews?: components['schemas']['previews'];
            url: string;
            buildPlan: components['schemas']['buildPlan'];
            renderSubdomainPolicy?: components['schemas']['renderSubdomainPolicy'];
        };
        maintenanceMode: {
            enabled: boolean;
            uri: string;
        };
        maxShutdownDelaySeconds: number;
        webServiceDetails: {
            autoscaling?: components['schemas']['autoscalingConfig'];
            cache?: components['schemas']['cache'];
            disk?: components['schemas']['disk'];
            env: components['schemas']['serviceEnv'];
            envSpecificDetails: components['schemas']['envSpecificDetails'];
            healthCheckPath: string;
            ipAllowList?: components['schemas']['cidrBlockAndDescription'][];
            maintenanceMode?: components['schemas']['maintenanceMode'];
            numInstances: number;
            openPorts: components['schemas']['serverPort'][];
            parentServer?: components['schemas']['resource'];
            plan: components['schemas']['plan'];
            pullRequestPreviewsEnabled?: components['schemas']['pullRequestPreviewsEnabled'];
            previews?: components['schemas']['previews'];
            region: components['schemas']['region'];
            runtime: components['schemas']['serviceRuntime'];
            sshAddress?: components['schemas']['sshAddress'];
            url: string;
            buildPlan: components['schemas']['buildPlan'];
            maxShutdownDelaySeconds?: components['schemas']['maxShutdownDelaySeconds'];
            renderSubdomainPolicy?: components['schemas']['renderSubdomainPolicy'];
        };
        envSpecificDetails: components['schemas']['dockerDetails'] | components['schemas']['nativeEnvironmentDetails'];
        envSpecificDetailsPATCH: components['schemas']['dockerDetailsPATCH'] | components['schemas']['nativeEnvironmentDetailsPATCH'];
        envSpecificDetailsPOST: components['schemas']['dockerDetailsPOST'] | components['schemas']['nativeEnvironmentDetailsPOST'];
        resource: {
            id: string;
            name: string;
        };
        privateServiceDetails: {
            autoscaling?: components['schemas']['autoscalingConfig'];
            disk?: components['schemas']['disk'];
            env: components['schemas']['serviceEnv'];
            envSpecificDetails: components['schemas']['envSpecificDetails'];
            numInstances: number;
            openPorts: components['schemas']['serverPort'][];
            parentServer?: components['schemas']['resource'];
            plan: components['schemas']['plan'];
            pullRequestPreviewsEnabled?: components['schemas']['pullRequestPreviewsEnabled'];
            previews?: components['schemas']['previews'];
            region: components['schemas']['region'];
            runtime: components['schemas']['serviceRuntime'];
            sshAddress?: components['schemas']['sshAddress'];
            url: string;
            buildPlan: components['schemas']['buildPlan'];
            maxShutdownDelaySeconds?: components['schemas']['maxShutdownDelaySeconds'];
        };
        serviceDisk: {
            name: string;
            mountPath: string;
            sizeGB?: number;
        };
        cache: {
            profile: string;
        };
        diskWithCursor: {
            disk: components['schemas']['diskDetails'];
            cursor: components['schemas']['cursor'];
        };
        instanceId: string;
        diskSnapshot: {
            createdAt?: string;
            snapshotKey?: string;
            instanceId?: components['schemas']['instanceId'];
        };
        snapshotRestorePOST: {
            snapshotKey: string;
            instanceId?: components['schemas']['instanceId'];
        };
        backgroundWorkerDetails: {
            autoscaling?: components['schemas']['autoscalingConfig'];
            disk?: components['schemas']['disk'];
            env: components['schemas']['serviceEnv'];
            envSpecificDetails: components['schemas']['envSpecificDetails'];
            numInstances: number;
            parentServer?: components['schemas']['resource'];
            plan: components['schemas']['plan'];
            pullRequestPreviewsEnabled?: components['schemas']['pullRequestPreviewsEnabled'];
            previews?: components['schemas']['previews'];
            region: components['schemas']['region'];
            runtime: components['schemas']['serviceRuntime'];
            sshAddress?: components['schemas']['sshAddress'];
            buildPlan: components['schemas']['buildPlan'];
            maxShutdownDelaySeconds?: components['schemas']['maxShutdownDelaySeconds'];
        };
        cronJobDetails: {
            env: components['schemas']['serviceEnv'];
            envSpecificDetails: components['schemas']['envSpecificDetails'];
            lastSuccessfulRunAt?: string;
            plan: components['schemas']['plan'];
            region: components['schemas']['region'];
            runtime: components['schemas']['serviceRuntime'];
            schedule: string;
            buildPlan: components['schemas']['buildPlan'];
        };
        serviceList: components['schemas']['serviceWithCursor'][];
        serviceWithCursor: {
            service: components['schemas']['service'];
            cursor: components['schemas']['cursor'];
        };
        servicePOST: {
            type: components['schemas']['serviceType'];
            name: string;
            ownerId: string;
            repo?: string;
            autoDeploy?: components['schemas']['autoDeploy'];
            autoDeployTrigger?: components['schemas']['autoDeployTrigger'];
            branch?: string;
            image?: components['schemas']['image'];
            buildFilter?: components['schemas']['buildFilter'];
            rootDir?: string;
            envVars?: components['schemas']['envVarInputArray'];
            secretFiles?: components['schemas']['secretFileInput'][];
            environmentId?: string;
            serviceDetails?: components['schemas']['staticSiteDetailsPOST'] | components['schemas']['webServiceDetailsPOST'] | components['schemas']['privateServiceDetailsPOST'] | components['schemas']['backgroundWorkerDetailsPOST'] | components['schemas']['cronJobDetailsPOST'];
        };
        dockerDetailsPOST: {
            dockerCommand?: string;
            dockerContext?: string;
            dockerfilePath?: string;
            registryCredentialId?: string;
        };
        nativeEnvironmentDetailsPOST: {
            buildCommand: string;
            startCommand: string;
        };
        staticSiteDetailsPOST: {
            buildCommand?: string;
            headers?: components['schemas']['headerInput'][];
            publishPath?: string;
            pullRequestPreviewsEnabled?: components['schemas']['pullRequestPreviewsEnabled'];
            previews?: components['schemas']['previews'];
            routes?: components['schemas']['routePost'][];
            renderSubdomainPolicy?: components['schemas']['renderSubdomainPolicy'];
            ipAllowList?: components['schemas']['cidrBlockAndDescription'][];
        };
        webServiceDetailsPOST: {
            autoscaling?: components['schemas']['autoscalingConfig'];
            disk?: components['schemas']['serviceDisk'];
            env?: components['schemas']['serviceEnv'];
            runtime: components['schemas']['serviceRuntime'];
            envSpecificDetails?: components['schemas']['envSpecificDetailsPOST'];
            healthCheckPath?: string;
            maintenanceMode?: components['schemas']['maintenanceMode'];
            numInstances?: number;
            plan?: components['schemas']['paidPlan'];
            preDeployCommand?: string;
            pullRequestPreviewsEnabled?: components['schemas']['pullRequestPreviewsEnabled'];
            previews?: components['schemas']['previews'];
            region?: components['schemas']['region'];
            maxShutdownDelaySeconds?: components['schemas']['maxShutdownDelaySeconds'];
            renderSubdomainPolicy?: components['schemas']['renderSubdomainPolicy'];
            ipAllowList?: components['schemas']['cidrBlockAndDescription'][];
        };
        privateServiceDetailsPOST: {
            autoscaling?: components['schemas']['autoscalingConfig'];
            disk?: components['schemas']['serviceDisk'];
            env?: components['schemas']['serviceEnv'];
            runtime: components['schemas']['serviceRuntime'];
            envSpecificDetails?: components['schemas']['envSpecificDetailsPOST'];
            numInstances: number;
            plan?: components['schemas']['paidPlan'];
            preDeployCommand?: string;
            pullRequestPreviewsEnabled?: components['schemas']['pullRequestPreviewsEnabled'];
            previews?: components['schemas']['previews'];
            region?: components['schemas']['region'];
            maxShutdownDelaySeconds?: components['schemas']['maxShutdownDelaySeconds'];
        };
        backgroundWorkerDetailsPOST: {
            autoscaling?: components['schemas']['autoscalingConfig'];
            disk?: components['schemas']['serviceDisk'];
            env?: components['schemas']['serviceEnv'];
            runtime: components['schemas']['serviceRuntime'];
            envSpecificDetails?: components['schemas']['envSpecificDetailsPOST'];
            numInstances: number;
            plan?: components['schemas']['paidPlan'];
            preDeployCommand?: string;
            pullRequestPreviewsEnabled?: components['schemas']['pullRequestPreviewsEnabled'];
            previews?: components['schemas']['previews'];
            region?: components['schemas']['region'];
            maxShutdownDelaySeconds?: components['schemas']['maxShutdownDelaySeconds'];
        };
        cronJobDetailsPOST: {
            env?: components['schemas']['serviceEnv'];
            runtime: components['schemas']['serviceRuntime'];
            envSpecificDetails?: components['schemas']['envSpecificDetails'];
            plan?: components['schemas']['paidPlan'];
            region?: components['schemas']['region'];
            schedule: string;
        };
        servicePATCH: {
            autoDeploy?: components['schemas']['autoDeploy'];
            autoDeployTrigger?: components['schemas']['autoDeployTrigger'];
            repo?: string;
            branch?: string;
            image?: components['schemas']['image'];
            name?: string;
            buildFilter?: components['schemas']['buildFilter'];
            rootDir?: string;
            serviceDetails?: components['schemas']['staticSiteDetailsPATCH'] | components['schemas']['webServiceDetailsPATCH'] | components['schemas']['privateServiceDetailsPATCH'] | components['schemas']['backgroundWorkerDetailsPATCH'] | components['schemas']['cronJobDetailsPATCH'];
        };
        dockerDetailsPATCH: {
            dockerCommand?: string;
            dockerContext?: string;
            dockerfilePath?: string;
            registryCredentialId?: string;
        };
        nativeEnvironmentDetailsPATCH: {
            buildCommand?: string;
            startCommand?: string;
        };
        staticSiteDetailsPATCH: {
            buildCommand?: string;
            publishPath?: string;
            pullRequestPreviewsEnabled?: components['schemas']['pullRequestPreviewsEnabled'];
            previews?: components['schemas']['previews'];
            renderSubdomainPolicy?: components['schemas']['renderSubdomainPolicy'];
            ipAllowList?: components['schemas']['cidrBlockAndDescription'][];
        };
        webServiceDetailsPATCH: {
            envSpecificDetails?: components['schemas']['envSpecificDetailsPATCH'];
            healthCheckPath?: string;
            maintenanceMode?: components['schemas']['maintenanceMode'];
            plan?: components['schemas']['paidPlan'];
            preDeployCommand?: string;
            pullRequestPreviewsEnabled?: components['schemas']['pullRequestPreviewsEnabled'];
            previews?: components['schemas']['previews'];
            runtime?: components['schemas']['serviceRuntime'];
            maxShutdownDelaySeconds?: components['schemas']['maxShutdownDelaySeconds'];
            renderSubdomainPolicy?: components['schemas']['renderSubdomainPolicy'];
            ipAllowList?: components['schemas']['cidrBlockAndDescription'][];
            cache?: components['schemas']['cache'];
        };
        privateServiceDetailsPATCH: {
            envSpecificDetails?: components['schemas']['envSpecificDetailsPATCH'];
            plan?: components['schemas']['paidPlan'];
            preDeployCommand?: string;
            pullRequestPreviewsEnabled?: components['schemas']['pullRequestPreviewsEnabled'];
            previews?: components['schemas']['previews'];
            runtime?: components['schemas']['serviceRuntime'];
            maxShutdownDelaySeconds?: components['schemas']['maxShutdownDelaySeconds'];
        };
        backgroundWorkerDetailsPATCH: {
            envSpecificDetails?: components['schemas']['envSpecificDetailsPATCH'];
            plan?: components['schemas']['paidPlan'];
            preDeployCommand?: string;
            pullRequestPreviewsEnabled?: components['schemas']['pullRequestPreviewsEnabled'];
            previews?: components['schemas']['previews'];
            runtime?: components['schemas']['serviceRuntime'];
            maxShutdownDelaySeconds?: components['schemas']['maxShutdownDelaySeconds'];
        };
        cronJobDetailsPATCH: {
            envSpecificDetails?: components['schemas']['envSpecificDetailsPATCH'];
            plan?: components['schemas']['paidPlan'];
            schedule?: string;
            runtime?: components['schemas']['serviceRuntime'];
        };
        envVarInputArray: components['schemas']['envVarInput'][];
        envVarInput: components['schemas']['envVarKeyValue'] | components['schemas']['envVarKeyGenerateValue'];
        envVarKeyValue: {
            key: string;
            value: string;
        };
        envVarValue: {
            value: string;
        };
        envVarKeyGenerateValue: {
            key: string;
            generateValue: boolean;
        };
        envVarGenerateValue: {
            generateValue: boolean;
        };
        addUpdateEnvVarInput: components['schemas']['envVarValue'] | components['schemas']['envVarGenerateValue'];
        previewInput: {
            imagePath: string;
            name?: string;
            plan?: components['schemas']['plan'];
        };
        plan: 'starter' | 'starter_plus' | 'standard' | 'standard_plus' | 'pro' | 'pro_plus' | 'pro_max' | 'pro_ultra' | 'free' | 'custom';
        header: {
            id: string;
            path: string;
            name: string;
            value: string;
        };
        headerInput: {
            path: string;
            name: string;
            value: string;
        };
        notificationOverrideWithCursor: {
            override: components['schemas']['notificationOverride'];
            cursor: components['schemas']['cursor'];
        };
        owner: {
            id: string;
            name: string;
            email: string;
            ipAllowList?: components['schemas']['cidrBlockAndDescription'][];
            twoFactorAuthEnabled?: boolean;
            type: 'user' | 'team';
        };
        teamMember: {
            userId: string;
            name: string;
            email: string;
            status: 'active' | 'inactive';
            role: string;
            mfaEnabled: boolean;
        };
        teamMembers: components['schemas']['teamMember'][];
        ownerWithCursor: {
            owner?: components['schemas']['owner'];
            cursor?: components['schemas']['cursor'];
        };
        route: {
            id: string;
            type: components['schemas']['routeType'];
            source: string;
            destination: string;
            priority: number;
        };
        headerWithCursor: {
            header: components['schemas']['header'];
            cursor: string;
        };
        routeWithCursor: {
            route: components['schemas']['route'];
            cursor: string;
        };
        routePost: {
            type: components['schemas']['routeType'];
            source: string;
            destination: string;
            priority?: number;
        };
        routePatch: {
            priority: number;
        };
        routePut: {
            type: components['schemas']['routeType'];
            source: string;
            destination: string;
        };
        routeType: 'redirect' | 'rewrite';
        serviceType: 'static_site' | 'web_service' | 'private_service' | 'background_worker' | 'cron_job';
        serviceTypeShort: 'static' | 'web' | 'pserv' | 'worker' | 'cron';
        serviceRuntime: 'docker' | 'elixir' | 'go' | 'node' | 'python' | 'ruby' | 'rust' | 'image';
        serviceEnv: 'docker' | 'elixir' | 'go' | 'node' | 'python' | 'ruby' | 'rust' | 'image';
        sshAddress: string;
        region: 'frankfurt' | 'oregon' | 'ohio' | 'singapore' | 'virginia';
        notifySetting: 'default' | 'notify' | 'ignore';
        suspenderType: 'admin' | 'billing' | 'user' | 'parent_service' | 'stuck_crashlooping' | 'hipaa_enablement' | 'unknown';
        deployStatus: 'created' | 'queued' | 'build_in_progress' | 'update_in_progress' | 'live' | 'deactivated' | 'build_failed' | 'update_failed' | 'canceled' | 'pre_deploy_in_progress' | 'pre_deploy_failed';
        deploy: {
            id: string;
            commit?: {
                id?: string;
                message?: string;
                createdAt?: string;
            };
            image?: {
                ref?: string;
                sha?: string;
                registryCredential?: string;
            };
            status?: components['schemas']['deployStatus'];
            trigger?: 'api' | 'blueprint_sync' | 'deploy_hook' | 'deployed_by_render' | 'manual' | 'other' | 'new_commit' | 'rollback' | 'service_resumed' | 'service_updated';
            startedAt?: string;
            finishedAt?: string;
            createdAt?: string;
            updatedAt?: string;
        };
        envVar: {
            key: string;
            value: string;
        };
        envVarWithCursor: {
            envVar: components['schemas']['envVar'];
            cursor: components['schemas']['cursor'];
        };
        customDomainWithCursor: {
            customDomain: components['schemas']['customDomain'];
            cursor: components['schemas']['cursor'];
        };
        customDomain: {
            id: string;
            name: string;
            domainType: 'apex' | 'subdomain';
            publicSuffix: string;
            redirectForName: string;
            verificationStatus: 'verified' | 'unverified';
            createdAt: string;
            server?: {
                id?: string;
                name?: string;
            };
        };
        serverPort: {
            port: number;
            protocol: 'TCP' | 'UDP';
        };
        error: {
            id?: string;
            message?: string;
        };
        pullRequestPreviewsEnabled: 'yes' | 'no';
        previews: {
            generation: 'off' | 'manual' | 'automatic';
        };
        buildPlan: 'starter' | 'performance';
        renderSubdomainPolicy: 'enabled' | 'disabled';
        keyValuePOSTInput: {
            name: string;
            ownerId: string;
            plan: components['schemas']['keyValuePlan'];
            region?: string;
            environmentId?: string;
            maxmemoryPolicy?: components['schemas']['maxmemoryPolicy'];
            ipAllowList?: components['schemas']['cidrBlockAndDescription'][];
        };
        keyValuePATCHInput: {
            name?: string;
            plan?: components['schemas']['keyValuePlan'];
            maxmemoryPolicy?: components['schemas']['maxmemoryPolicy'];
            ipAllowList?: components['schemas']['cidrBlockAndDescription'][];
        };
        maxmemoryPolicy: 'noeviction' | 'allkeys_lfu' | 'allkeys_lru' | 'allkeys_random' | 'volatile_lfu' | 'volatile_lru' | 'volatile_random' | 'volatile_ttl';
        keyValue: {
            id: string;
            createdAt: string;
            updatedAt: string;
            status: components['schemas']['databaseStatus'];
            region: components['schemas']['region'];
            plan: components['schemas']['keyValuePlan'];
            name: string;
            owner: components['schemas']['owner'];
            options: components['schemas']['keyValueOptions'];
            ipAllowList: components['schemas']['cidrBlockAndDescription'][];
            environmentId?: string;
            version: string;
            dashboardUrl: string;
        };
        keyValueWithCursor: {
            keyValue: components['schemas']['keyValue'];
            cursor: components['schemas']['cursor'];
        };
        keyValueDetail: {
            id: string;
            createdAt: string;
            updatedAt: string;
            status: components['schemas']['databaseStatus'];
            region: components['schemas']['region'];
            plan: components['schemas']['keyValuePlan'];
            name: string;
            owner: components['schemas']['owner'];
            options: components['schemas']['keyValueOptions'];
            ipAllowList: components['schemas']['cidrBlockAndDescription'][];
            environmentId?: string;
            version: string;
            maintenance?: components['schemas']['maintenanceRun'];
        };
        keyValueConnectionInfo: {
            internalConnectionString: string;
            externalConnectionString: string;
            cliCommand: string;
        };
        keyValueOptions: {
            maxmemoryPolicy?: string;
        };
        cidrBlockAndDescription: {
            cidrBlock: string;
            description: string;
        };
        keyValuePlan: 'free' | 'starter' | 'standard' | 'pro' | 'pro_plus' | 'custom';
        redisPOSTInput: {
            name: string;
            ownerId: string;
            plan: components['schemas']['redisPlan'];
            region?: string;
            environmentId?: string;
            maxmemoryPolicy?: components['schemas']['maxmemoryPolicy'];
            ipAllowList?: components['schemas']['cidrBlockAndDescription'][];
        };
        redisPATCHInput: {
            name?: string;
            plan?: components['schemas']['redisPlan'];
            maxmemoryPolicy?: components['schemas']['maxmemoryPolicy'];
            ipAllowList?: components['schemas']['cidrBlockAndDescription'][];
        };
        redis: {
            id: string;
            createdAt: string;
            updatedAt: string;
            status: components['schemas']['databaseStatus'];
            region: components['schemas']['region'];
            plan: components['schemas']['redisPlan'];
            name: string;
            owner: components['schemas']['owner'];
            options: components['schemas']['redisOptions'];
            ipAllowList: components['schemas']['cidrBlockAndDescription'][];
            environmentId?: string;
            version: string;
            dashboardUrl: string;
        };
        redisWithCursor: {
            redis: components['schemas']['redis'];
            cursor: components['schemas']['cursor'];
        };
        redisDetail: {
            id: string;
            createdAt: string;
            updatedAt: string;
            status: components['schemas']['databaseStatus'];
            region: components['schemas']['region'];
            plan: components['schemas']['redisPlan'];
            name: string;
            owner: components['schemas']['owner'];
            options: components['schemas']['redisOptions'];
            ipAllowList: components['schemas']['cidrBlockAndDescription'][];
            environmentId?: string;
            version: string;
            maintenance?: components['schemas']['maintenanceRun'];
        };
        redisConnectionInfo: {
            internalConnectionString: string;
            externalConnectionString: string;
            redisCLICommand: string;
        };
        redisOptions: {
            maxmemoryPolicy?: string;
        };
        redisPlan: 'free' | 'starter' | 'standard' | 'pro' | 'pro_plus' | 'custom';
        databaseStatus: 'creating' | 'available' | 'unavailable' | 'config_restart' | 'suspended' | 'maintenance_scheduled' | 'maintenance_in_progress' | 'recovery_failed' | 'recovery_in_progress' | 'unknown' | 'updating_instance';
        projectWithCursor: {
            project: components['schemas']['project'];
            cursor: components['schemas']['cursor'];
        };
        project: {
            id: string;
            createdAt: string;
            updatedAt: string;
            name: string;
            owner: components['schemas']['owner'];
            environmentIds: string[];
        };
        projectPOSTInput: {
            name: string;
            ownerId: string;
            environments: components['schemas']['projectPOSTEnvironmentInput'][];
        };
        projectPATCHInput: {
            name?: string;
        };
        projectPOSTEnvironmentInput: {
            name: string;
            protectedStatus?: components['schemas']['protectedStatus'];
            networkIsolationEnabled?: components['schemas']['networkIsolationEnabled'];
            ipAllowList?: components['schemas']['cidrBlockAndDescription'][];
        };
        environmentPOSTInput: {
            name: string;
            projectId: string;
            protectedStatus?: components['schemas']['protectedStatus'];
            networkIsolationEnabled?: components['schemas']['networkIsolationEnabled'];
            ipAllowList?: components['schemas']['cidrBlockAndDescription'][];
        };
        environmentResourcesPOSTInput: {
            resourceIds: string[];
        };
        environmentPATCHInput: {
            name?: string;
            networkIsolationEnabled?: components['schemas']['networkIsolationEnabled'];
            protectedStatus?: components['schemas']['protectedStatus'];
            ipAllowList?: components['schemas']['cidrBlockAndDescription'][];
        };
        environment: {
            id: string;
            name: string;
            projectId: string;
            databasesIds: string[];
            ipAllowList?: components['schemas']['cidrBlockAndDescription'][];
            redisIds: string[];
            serviceIds: string[];
            envGroupIds: string[];
            protectedStatus: components['schemas']['protectedStatus'];
            networkIsolationEnabled: components['schemas']['networkIsolationEnabled'];
        };
        environmentWithCursor: {
            environment: components['schemas']['environment'];
            cursor: components['schemas']['cursor'];
        };
        protectedStatus: 'unprotected' | 'protected';
        networkIsolationEnabled: boolean;
        envGroupPOSTInput: {
            name: string;
            ownerId: string;
            envVars: components['schemas']['envVarInputArray'];
            secretFiles?: components['schemas']['secretFileInput'][];
            serviceIds?: string[];
            environmentId?: string;
        };
        envGroupPATCHInput: {
            name: string;
        };
        secretFileInput: {
            name: string;
            content: string;
        };
        envGroup: components['schemas']['envGroupMeta'] & {
            envVars: components['schemas']['envVar'][];
            secretFiles: components['schemas']['secretFile'][];
        };
        envGroupMeta: {
            id: string;
            name: string;
            ownerId: string;
            createdAt: string;
            updatedAt: string;
            serviceLinks: components['schemas']['envGroupLink'][];
            environmentId?: string;
        };
        secretFile: {
            name: string;
            content: string;
        };
        secretFileWithCursor: {
            secretFile: components['schemas']['secretFile'];
            cursor: components['schemas']['cursor'];
        };
        envGroupLink: {
            id: string;
            name: string;
            type: components['schemas']['serviceTypeShort'];
        };
        postgresPOSTInput: {
            databaseName: string;
            databaseUser: string;
            datadogAPIKey?: string;
            datadogSite?: string;
            name: string;
            enableHighAvailability: boolean;
            environmentId?: string;
            ownerId: string;
            plan: components['schemas']['postgresPlans'];
            diskSizeGB?: number;
            region?: string;
            ipAllowList?: components['schemas']['cidrBlockAndDescription'][];
            readReplicas?: components['schemas']['readReplicasInput'];
            version: components['schemas']['postgresVersion'];
        };
        postgresPATCHInput: {
            name?: string;
            plan?: components['schemas']['postgresPlans'];
            diskSizeGB?: number;
            enableHighAvailability?: boolean;
            datadogAPIKey?: string;
            datadogSite?: string;
            ipAllowList?: components['schemas']['cidrBlockAndDescription'][];
            readReplicas?: components['schemas']['readReplicasInput'];
        };
        readReplicas: components['schemas']['readReplica'][];
        readReplica: {
            id: string;
            name: string;
        };
        readReplicasInput: components['schemas']['readReplicaInput'][];
        readReplicaInput: {
            name: string;
        };
        postgresConnectionInfo: {
            password: string;
            internalConnectionString: string;
            externalConnectionString: string;
            psqlCommand: string;
        };
        postgresWithCursor: {
            postgres: components['schemas']['postgres'];
            cursor: components['schemas']['cursor'];
        };
        postgres: {
            id: string;
            ipAllowList: components['schemas']['cidrBlockAndDescription'][];
            createdAt: string;
            updatedAt: string;
            expiresAt?: string;
            databaseName: string;
            databaseUser: string;
            environmentId?: string;
            highAvailabilityEnabled: boolean;
            name: string;
            owner: components['schemas']['owner'];
            plan: components['schemas']['postgresPlans'];
            diskSizeGB?: number;
            primaryPostgresID?: string;
            region: components['schemas']['region'];
            readReplicas: components['schemas']['readReplicas'];
            role: components['schemas']['databaseRole'];
            status: components['schemas']['databaseStatus'];
            version: components['schemas']['postgresVersion'];
            suspended: 'suspended' | 'not_suspended';
            suspenders: components['schemas']['suspenderType'][];
            dashboardUrl: string;
        };
        postgresDetail: {
            id: string;
            ipAllowList: components['schemas']['cidrBlockAndDescription'][];
            createdAt: string;
            updatedAt: string;
            expiresAt?: string;
            dashboardUrl: string;
            databaseName: string;
            databaseUser: string;
            environmentId?: string;
            highAvailabilityEnabled: boolean;
            maintenance?: components['schemas']['maintenanceRun'];
            name: string;
            owner: components['schemas']['owner'];
            plan: components['schemas']['postgresPlans'];
            diskSizeGB?: number;
            primaryPostgresID?: string;
            region: components['schemas']['region'];
            readReplicas: components['schemas']['readReplicas'];
            role: components['schemas']['databaseRole'];
            status: components['schemas']['databaseStatus'];
            version: components['schemas']['postgresVersion'];
            suspended: 'suspended' | 'not_suspended';
            suspenders: components['schemas']['suspenderType'][];
        };
        postgresVersion: '11' | '12' | '13' | '14' | '15' | '16' | '17';
        databaseRole: 'primary' | 'replica';
        paidPlan: 'starter' | 'standard' | 'pro' | 'pro_plus' | 'pro_max' | 'pro_ultra';
        cronJobRun: {
            id: string;
            status: 'pending' | 'successful' | 'unsuccessful' | 'canceled';
            startedAt?: string;
            finishedAt?: string;
            triggeredBy?: string;
            canceledBy?: string;
        };
        blueprintWithCursor: {
            blueprint: components['schemas']['blueprint'];
            cursor: components['schemas']['cursor'];
        };
        syncWithCursor: {
            sync: components['schemas']['sync'];
            cursor: components['schemas']['cursor'];
        };
        serviceEventWithCursor: {
            event: components['schemas']['serviceEvent'];
        };
        jobWithCursor: {
            job: components['schemas']['job'];
            cursor: components['schemas']['cursor'];
        };
        user: {
            email: string;
            name: string;
        };
        webhookWithCursor: {
            webhook: components['schemas']['webhook'];
            cursor: components['schemas']['cursor'];
        };
        webhookEventWithCursor: {
            webhookEvent: components['schemas']['webhookEvent'];
            cursor: components['schemas']['cursor'];
        };
        serviceInstance: {
            id: string;
            createdAt: string;
        };
        blueprintId: string;
        status: 'created' | 'paused' | 'in_sync' | 'syncing' | 'error';
        autoSync: boolean;
        blueprint: {
            id: components['schemas']['blueprintId'];
            name: string;
            status: components['schemas']['status'];
            autoSync: components['schemas']['autoSync'];
            repo: string;
            branch: string;
            lastSync?: string;
        };
        resourceRef: {
            id: string;
            name: string;
            type: 'static_site' | 'web_service' | 'private_service' | 'background_worker' | 'cron_job' | 'redis' | 'key_value' | 'postgres' | 'environment_group';
        };
        blueprintDetail: {
            id: components['schemas']['blueprintId'];
            name: string;
            status: components['schemas']['status'];
            autoSync: components['schemas']['autoSync'];
            repo: string;
            branch: string;
            lastSync?: string;
            resources: components['schemas']['resourceRef'][];
        };
        blueprintPATCH: {
            name?: string;
            autoSync?: components['schemas']['autoSync'];
        };
        syncId: string;
        commitRef: {
            id: string;
        };
        syncState: 'created' | 'pending' | 'running' | 'error' | 'success';
        sync: {
            id: components['schemas']['syncId'];
            commit: components['schemas']['commitRef'];
            startedAt?: string;
            completedAt?: string;
            state: components['schemas']['syncState'];
        };
        diskId: string;
        diskDetails: {
            id: components['schemas']['diskId'];
            name: string;
            sizeGB: number;
            mountPath: string;
            serviceId?: string;
            createdAt: string;
            updatedAt: string;
        };
        diskPOST: {
            name: string;
            sizeGB: number;
            mountPath: string;
            serviceId: string;
        };
        diskPATCH: {
            name?: string;
            sizeGB?: number;
            mountPath?: string;
        };
        notifySettingV2: 'none' | 'failure' | 'all';
        notificationSetting: {
            ownerId: string;
            slackEnabled: boolean;
            emailEnabled: boolean;
            previewNotificationsEnabled: boolean;
            notificationsToSend: components['schemas']['notifySettingV2'];
        };
        notificationSettingPATCH: {
            emailEnabled?: boolean;
            previewNotificationsEnabled?: boolean;
            notificationsToSend?: components['schemas']['notifySettingV2'];
        };
        notifyPreviewOverride: 'default' | 'false' | 'true';
        notifyOverride: 'default' | 'none' | 'failure' | 'all';
        notificationOverride: {
            serviceId: string;
            previewNotificationsEnabled: components['schemas']['notifyPreviewOverride'];
            notificationsToSend: components['schemas']['notifyOverride'];
        };
        notificationServiceOverride: {
            serviceId: string;
            previewNotificationsEnabled: components['schemas']['notifyPreviewOverride'];
            notificationsToSend: components['schemas']['notifyOverride'];
        };
        notificationServiceOverridePATCH: {
            previewNotificationsEnabled?: components['schemas']['notifyPreviewOverride'];
            notificationsToSend?: components['schemas']['notifyOverride'];
        };
        autoscalingCriteriaPercentage: {
            enabled: boolean;
            percentage: number;
        };
        autoscalingCriteria: {
            cpu: components['schemas']['autoscalingCriteriaPercentage'];
            memory: components['schemas']['autoscalingCriteriaPercentage'];
        };
        autoscalingConfig: {
            enabled: boolean;
            min: number;
            max: number;
            criteria: components['schemas']['autoscalingCriteria'];
        };
        disk: {
            id: components['schemas']['diskId'];
            name: string;
            sizeGB: number;
            mountPath: string;
        };
        serviceEventType: 'autoscaling_config_changed' | 'autoscaling_ended' | 'autoscaling_started' | 'branch_deleted' | 'build_ended' | 'build_started' | 'commit_ignored' | 'cron_job_run_ended' | 'cron_job_run_started' | 'deploy_ended' | 'deploy_started' | 'disk_created' | 'disk_updated' | 'disk_deleted' | 'image_pull_failed' | 'initial_deploy_hook_ended' | 'initial_deploy_hook_started' | 'instance_count_changed' | 'job_run_ended' | 'maintenance_mode_enabled' | 'maintenance_mode_uri_updated' | 'maintenance_ended' | 'maintenance_started' | 'pipeline_minutes_exhausted' | 'plan_changed' | 'pre_deploy_ended' | 'pre_deploy_started' | 'server_available' | 'server_failed' | 'server_hardware_failure' | 'server_restarted' | 'service_resumed' | 'service_suspended' | 'suspender_added' | 'suspender_removed' | 'zero_downtime_redeploy_ended' | 'zero_downtime_redeploy_started';
        eventId: string;
        autoscalingConfigChangedEvent: {
            fromConfig?: components['schemas']['autoscalingConfig'];
            toConfig: components['schemas']['autoscalingConfig'];
        };
        autoscalingEndedEvent: {
            fromInstances: number;
            toInstances: number;
        };
        autoscalingStartedEvent: {
            fromInstances: number;
            toInstances: number;
            currentCPU?: number;
            targetCPU?: number;
            currentMemory?: number;
            targetMemory?: number;
        };
        branchDeletedEvent: {
            deletedBranch: string;
            newBranch: string;
        };
        eventStatus: 'succeeded' | 'failed' | 'canceled';
        buildDeployEndReasonID: {
            id: string;
        };
        oomKilled: {
            memoryLimit: string;
        };
        failureReason: {
            evicted: boolean;
            nonZeroExit?: number;
            earlyExit?: boolean;
            oomKilled?: components['schemas']['oomKilled'];
            timedOutSeconds?: number;
            unhealthy?: string;
            timedOutReason?: string;
        };
        buildDeployEndReason: {
            buildFailed?: components['schemas']['buildDeployEndReasonID'];
            newBuild?: components['schemas']['buildDeployEndReasonID'];
            newDeploy?: components['schemas']['buildDeployEndReasonID'];
            failure?: components['schemas']['failureReason'];
        };
        buildEndedEvent: {
            buildId: string;
            buildStatus: components['schemas']['eventStatus'];
            reason: components['schemas']['buildDeployEndReason'];
            status: number;
        };
        'schemas-user': {
            id: string;
            email: string;
        };
        buildDeployTrigger: {
            firstBuild: boolean;
            envUpdated: boolean;
            manual: boolean;
            user?: components['schemas']['schemas-user'];
            updatedProperty?: string;
            newCommit?: string;
            deployedByRender: boolean;
            clearCache: boolean;
            rollback: boolean;
            rollbackTargetDeployId?: string;
        };
        buildStartedEvent: {
            buildId: string;
            trigger: components['schemas']['buildDeployTrigger'];
        };
        commitIgnoredEvent: {
            id: string;
            url: string;
        };
        cronJobRunStatus: 'canceled' | 'pending' | 'successful' | 'unsuccessful';
        cronJobRunEndedEvent: {
            cronJobRunId: string;
            status: components['schemas']['cronJobRunStatus'];
            reason?: components['schemas']['failureReason'];
            user?: components['schemas']['schemas-user'];
        };
        cronJobRunStartedEvent: {
            cronJobRunId: string;
        };
        deployEndedEvent: {
            deployId: string;
            reason: components['schemas']['buildDeployEndReason'];
            deployStatus: components['schemas']['eventStatus'];
            status: number;
        };
        deployStartedEvent: {
            deployId: string;
            trigger: components['schemas']['buildDeployTrigger'];
        };
        diskCreatedEvent: {
            diskId: components['schemas']['diskId'];
            sizeGB: number;
        };
        diskUpdatedEvent: {
            diskId: components['schemas']['diskId'];
            fromSizeGB: number;
            toSizeGB: number;
        };
        diskDeletedEvent: {
            diskId: components['schemas']['diskId'];
        };
        imagePullFailedEvent: {
            message: string;
            imageURL: string;
        };
        initialDeployHookStartedEvent: {
            deployId: string;
        };
        initialDeployHookEndedEvent: {
            deployId: string;
        };
        instanceCountChangedEvent: {
            fromInstances: number;
            toInstances: number;
        };
        jobId: string;
        jobStatus: 'pending' | 'running' | 'succeeded' | 'failed' | 'canceled';
        jobRunEndedEvent: {
            jobId: components['schemas']['jobId'];
            status: components['schemas']['jobStatus'];
            reason?: components['schemas']['failureReason'];
        };
        maintenanceModeEnabledEvent: {
            enabled: boolean;
        };
        maintenanceModeURIUpdatedEvent: {
            fromURI: string;
            toURI: string;
        };
        maintenanceEndedEvent: Record<string, never>;
        maintenanceTrigger: {
            user?: components['schemas']['schemas-user'];
            manual: boolean;
            startedByRender: boolean;
        };
        maintenanceStartedEvent: {
            trigger: components['schemas']['maintenanceTrigger'];
        };
        pipelineMinutesExhaustedEvent: {
            buildId: string;
            trigger: components['schemas']['buildDeployTrigger'];
        };
        planChangedEvent: {
            from: string;
            to: string;
        };
        preDeployEndedEvent: {
            deployCommandExecutionId: string;
            deployId: string;
            preDeployStatus: components['schemas']['eventStatus'];
            reason: components['schemas']['buildDeployEndReason'];
            status: number;
        };
        preDeployStartedEvent: {
            deployCommandExecutionId: string;
            deployId: string;
        };
        serverAvailableEvent: Record<string, never>;
        'schemas-instanceId': string;
        serverFailedEvent: {
            instanceID?: components['schemas']['schemas-instanceId'];
            reason?: components['schemas']['failureReason'];
        };
        serverHardwareFailureEvent: Record<string, never>;
        serverRestartedEvent: {
            triggeredByUser: string | null;
        };
        serviceResumedEvent: Record<string, never>;
        serviceSuspendedEvent: Record<string, never>;
        suspenderAddedEvent: {
            actor: string;
            suspendedByUser?: components['schemas']['schemas-user'];
        };
        suspenderRemovedEvent: {
            actor: string;
            resumedByUser?: components['schemas']['schemas-user'];
        };
        zeroDowntimeRedeployEndedEvent: Record<string, never>;
        zeroDowntimeRedeployStartedEvent: {
            trigger: string;
        };
        edgeCacheTrigger: {
            manual: boolean;
            user?: components['schemas']['schemas-user'];
            system: boolean;
        };
        edgeCacheDisabledEvent: {
            trigger: components['schemas']['edgeCacheTrigger'];
        };
        edgeCacheEnabledEvent: {
            trigger: components['schemas']['edgeCacheTrigger'];
        };
        edgeCachePurgedEvent: {
            trigger: components['schemas']['edgeCacheTrigger'];
        };
        serviceEventDetails: components['schemas']['autoscalingConfigChangedEvent'] | components['schemas']['autoscalingEndedEvent'] | components['schemas']['autoscalingStartedEvent'] | components['schemas']['branchDeletedEvent'] | components['schemas']['buildEndedEvent'] | components['schemas']['buildStartedEvent'] | components['schemas']['commitIgnoredEvent'] | components['schemas']['cronJobRunEndedEvent'] | components['schemas']['cronJobRunStartedEvent'] | components['schemas']['deployEndedEvent'] | components['schemas']['deployStartedEvent'] | components['schemas']['diskCreatedEvent'] | components['schemas']['diskUpdatedEvent'] | components['schemas']['diskDeletedEvent'] | components['schemas']['imagePullFailedEvent'] | components['schemas']['initialDeployHookStartedEvent'] | components['schemas']['initialDeployHookEndedEvent'] | components['schemas']['instanceCountChangedEvent'] | components['schemas']['jobRunEndedEvent'] | components['schemas']['maintenanceModeEnabledEvent'] | components['schemas']['maintenanceModeURIUpdatedEvent'] | components['schemas']['maintenanceEndedEvent'] | components['schemas']['maintenanceStartedEvent'] | components['schemas']['pipelineMinutesExhaustedEvent'] | components['schemas']['planChangedEvent'] | components['schemas']['preDeployEndedEvent'] | components['schemas']['preDeployStartedEvent'] | components['schemas']['serverAvailableEvent'] | components['schemas']['serverFailedEvent'] | components['schemas']['serverHardwareFailureEvent'] | components['schemas']['serverRestartedEvent'] | components['schemas']['serviceResumedEvent'] | components['schemas']['serviceSuspendedEvent'] | components['schemas']['suspenderAddedEvent'] | components['schemas']['suspenderRemovedEvent'] | components['schemas']['zeroDowntimeRedeployEndedEvent'] | components['schemas']['zeroDowntimeRedeployStartedEvent'] | components['schemas']['edgeCacheDisabledEvent'] | components['schemas']['edgeCacheEnabledEvent'] | components['schemas']['edgeCachePurgedEvent'];
        serviceEvent: {
            id: components['schemas']['eventId'];
            timestamp: string;
            serviceId: string;
            type: components['schemas']['serviceEventType'];
            details: components['schemas']['serviceEventDetails'];
        };
        job: {
            id: components['schemas']['jobId'];
            serviceId: string;
            startCommand: string;
            planId: string;
            status?: components['schemas']['jobStatus'];
            createdAt: string;
            startedAt?: string;
            finishedAt?: string;
        };
        eventType: 'autoscaling_config_changed' | 'autoscaling_ended' | 'autoscaling_started' | 'branch_deleted' | 'build_ended' | 'build_started' | 'commit_ignored' | 'cron_job_run_ended' | 'cron_job_run_started' | 'deploy_ended' | 'deploy_started' | 'disk_created' | 'disk_updated' | 'disk_deleted' | 'image_pull_failed' | 'instance_count_changed' | 'job_run_ended' | 'maintenance_mode_enabled' | 'maintenance_mode_uri_updated' | 'maintenance_ended' | 'maintenance_started' | 'pipeline_minutes_exhausted' | 'plan_changed' | 'pre_deploy_ended' | 'pre_deploy_started' | 'server_available' | 'server_failed' | 'server_hardware_failure' | 'server_restarted' | 'service_resumed' | 'service_suspended' | 'zero_downtime_redeploy_ended' | 'zero_downtime_redeploy_started' | 'edge_cache_enabled' | 'edge_cache_disabled' | 'edge_cache_purged' | 'postgres_available' | 'postgres_backup_completed' | 'postgres_backup_failed' | 'postgres_backup_started' | 'postgres_cluster_leader_changed' | 'postgres_created' | 'postgres_disk_size_changed' | 'postgres_ha_status_changed' | 'postgres_restarted' | 'postgres_unavailable' | 'postgres_upgrade_failed' | 'postgres_upgrade_started' | 'postgres_upgrade_succeeded' | 'postgres_restore_failed' | 'postgres_restore_succeeded' | 'postgres_read_replicas_changed' | 'postgres_pitr_checkpoint_started' | 'postgres_pitr_checkpoint_failed' | 'postgres_pitr_checkpoint_completed' | 'postgres_read_replica_stale' | 'postgres_wal_archive_failed' | 'key_value_available' | 'key_value_config_restart' | 'key_value_unhealthy';
        postgresAvailableEvent: Record<string, never>;
        postgresBackupCompletedEvent: Record<string, never>;
        postgresBackupFailedEvent: Record<string, never>;
        postgresBackupStartedEvent: Record<string, never>;
        postgresClusterLeaderChangedEvent: {
            leaderId?: string;
        };
        postgresCreatedEvent: {
            user?: components['schemas']['schemas-user'];
        };
        postgresDiskSizeChangedEvent: {
            user?: components['schemas']['schemas-user'];
            fromDiskSize: number;
            toDiskSize: number;
        };
        postgresHaStatusChangedEvent: {
            fromStatus: string;
            toStatus: string;
        };
        postgresReadReplicasChangedEvent: {
            fromReplicas: number;
            toReplicas: number;
        };
        postgresRestartedEvent: {
            user?: components['schemas']['schemas-user'];
        };
        postgresUnavailableEvent: Record<string, never>;
        postgresUpgradeFailedEvent: {
            fromVersion: string;
            toVersion: string;
        };
        postgresUpgradeStartedEvent: {
            user?: components['schemas']['schemas-user'];
            fromVersion: string;
            toVersion: string;
        };
        postgresUpgradeSucceededEvent: {
            fromVersion: string;
            toVersion: string;
        };
        postgresPITRCheckpointStartedEvent: Record<string, never>;
        postgresPITRCheckpointFailedEvent: Record<string, never>;
        postgresPITRCheckpointCompletedEvent: Record<string, never>;
        postgresReadReplicaStale: Record<string, never>;
        postgresEventDetails: components['schemas']['postgresAvailableEvent'] | components['schemas']['postgresBackupCompletedEvent'] | components['schemas']['postgresBackupFailedEvent'] | components['schemas']['postgresBackupStartedEvent'] | components['schemas']['postgresClusterLeaderChangedEvent'] | components['schemas']['postgresCreatedEvent'] | components['schemas']['postgresDiskSizeChangedEvent'] | components['schemas']['postgresHaStatusChangedEvent'] | components['schemas']['postgresReadReplicasChangedEvent'] | components['schemas']['postgresRestartedEvent'] | components['schemas']['postgresUnavailableEvent'] | components['schemas']['postgresUpgradeFailedEvent'] | components['schemas']['postgresUpgradeStartedEvent'] | components['schemas']['postgresUpgradeSucceededEvent'] | components['schemas']['postgresPITRCheckpointStartedEvent'] | components['schemas']['postgresPITRCheckpointFailedEvent'] | components['schemas']['postgresPITRCheckpointCompletedEvent'] | components['schemas']['postgresReadReplicaStale'];
        keyValueAvailableEvent: Record<string, never>;
        keyValueConfigRestartEvent: {
            reason: string;
            message: string;
        };
        keyValueUnhealthyEvent: Record<string, never>;
        keyValueEventDetails: components['schemas']['keyValueAvailableEvent'] | components['schemas']['keyValueConfigRestartEvent'] | components['schemas']['keyValueUnhealthyEvent'];
        eventDetails: components['schemas']['serviceEventDetails'] | components['schemas']['postgresEventDetails'] | components['schemas']['keyValueEventDetails'];
        event: {
            id: components['schemas']['eventId'];
            timestamp: string;
            serviceId: string;
            type: components['schemas']['eventType'];
            details: components['schemas']['eventDetails'];
        };
        logDirection: 'forward' | 'backward';
        logLabelName: 'resource' | 'instance' | 'host' | 'statusCode' | 'method' | 'level' | 'workflowService' | 'workflowVeresion' | 'task' | 'taskRun' | 'type' | 'text' | 'path' | 'blocked';
        logLabel: {
            name: components['schemas']['logLabelName'];
            value: string;
        };
        log: {
            id: string;
            message: string;
            timestamp: string;
            labels: components['schemas']['logLabel'][];
        };
        logStreamPreviewSetting: 'send' | 'drop';
        ownerLogStreamSetting: {
            ownerId?: string;
            endpoint?: string;
            preview?: components['schemas']['logStreamPreviewSetting'];
        };
        logStreamEndpoint: string;
        logStreamToken: string;
        logStreamOwnerUpdate: {
            endpoint?: components['schemas']['logStreamEndpoint'];
            token?: components['schemas']['logStreamToken'];
            preview: components['schemas']['logStreamPreviewSetting'];
        };
        logStreamSetting: 'send' | 'drop';
        resourceLogStreamSetting: {
            resourceId?: string;
            endpoint?: string;
            setting?: components['schemas']['logStreamSetting'];
        };
        logStreamResourceUpdate: {
            endpoint?: components['schemas']['logStreamEndpoint'];
            token?: components['schemas']['logStreamToken'];
            setting: components['schemas']['logStreamSetting'];
        };
        otelProviderType: 'BETTER_STACK' | 'GRAFANA' | 'DATADOG' | 'NEW_RELIC' | 'HONEYCOMB' | 'CUSTOM';
        metricsStream: {
            ownerId: string;
            provider: components['schemas']['otelProviderType'];
            url: string;
        };
        metricsStreamInput: {
            provider?: components['schemas']['otelProviderType'];
            url?: string;
            token?: string;
        };
        label: {
            field: string;
            value: string;
        };
        timeSeriesValue: {
            timestamp: string;
            value: number;
        };
        unit: string;
        timeSeries: {
            labels: components['schemas']['label'][];
            values: components['schemas']['timeSeriesValue'][];
            unit: components['schemas']['unit'];
        };
        timeSeriesCollection: components['schemas']['timeSeries'][];
        filterApplicationValuesCollection: {
            filter?: 'instance';
            values?: string[];
        }[];
        filterHTTPValuesCollection: {
            filter?: 'host' | 'statusCode';
            values?: string[];
        }[];
        filterPathValuesCollection: string[];
        maintenanceRunId: string;
        maintenanceState: 'scheduled' | 'in_progress' | 'user_fix_required' | 'cancelled' | 'succeeded' | 'failed';
        maintenanceRun: {
            id: components['schemas']['maintenanceRunId'];
            type: string;
            scheduledAt: string;
            pendingMaintenanceBy?: string;
            state: components['schemas']['maintenanceState'];
        };
        postgresPlans: 'free' | 'starter' | 'standard' | 'pro' | 'pro_plus' | 'custom' | 'basic_256mb' | 'basic_1gb' | 'basic_4gb' | 'pro_4gb' | 'pro_8gb' | 'pro_16gb' | 'pro_32gb' | 'pro_64gb' | 'pro_128gb' | 'pro_192gb' | 'pro_256gb' | 'pro_384gb' | 'pro_512gb' | 'accelerated_16gb' | 'accelerated_32gb' | 'accelerated_64gb' | 'accelerated_128gb' | 'accelerated_256gb' | 'accelerated_384gb' | 'accelerated_512gb' | 'accelerated_768gb' | 'accelerated_1024gb';
        recoveryInfo: {
            recoveryStatus: 'AVAILABLE' | 'BACKUP_NOT_READY' | 'NOT_AVAILABLE';
            startsAt?: string;
        };
        recoveryInput: {
            restoreName?: string;
            restoreTime: string;
            datadogApiKey?: string;
            datadogSite?: string;
            plan?: string;
            environmentId?: string;
        };
        postgresExport: {
            id: string;
            createdAt: string;
            url?: string;
        };
        maintenanceResourceId: string;
        maintenanceRunWithResource: {
            id: components['schemas']['maintenanceRunId'];
            type: string;
            scheduledAt: string;
            pendingMaintenanceBy?: string;
            state: components['schemas']['maintenanceState'];
            resourceId: components['schemas']['maintenanceResourceId'];
        };
        maintenanceRunPATCH: {
            scheduledAt?: string;
        };
        webhookId: string;
        eventFilter: components['schemas']['eventType'][];
        webhook: {
            id: components['schemas']['webhookId'];
            url: string;
            name: string;
            secret: string;
            enabled: boolean;
            eventFilter: components['schemas']['eventFilter'];
        };
        webhookPOSTInput: {
            ownerId: string;
            url: string;
            name: string;
            enabled: boolean;
            eventFilter: components['schemas']['eventFilter'];
        };
        webhookPATCHInput: {
            name?: string;
            url?: string;
            enabled?: boolean;
            eventFilter?: components['schemas']['eventFilter'];
        };
        webhookEvent: {
            id: string;
            eventId: string;
            eventType: components['schemas']['eventType'];
            sentAt: string;
            statusCode?: number;
            responseBody?: string;
            error?: string;
        };
        Runtime: 'elixir' | 'go' | 'node' | 'python' | 'ruby';
        BuildConfig: {
            branch?: string;
            buildCommand: string;
            repo: string;
            rootDir?: string;
            runtime: components['schemas']['Runtime'];
        };
        Region: 'frankfurt' | 'oregon' | 'ohio' | 'singapore' | 'virginia';
        Workflow: {
            id: string;
            name: string;
            ownerId: string;
            createdAt: string;
            updatedAt: string;
            buildConfig: components['schemas']['BuildConfig'];
            runCommand: string;
            region: components['schemas']['Region'];
            environmentId?: string;
            slug?: string;
        };
        WorkflowCreate: {
            name: string;
            ownerId: string;
            buildConfig: components['schemas']['BuildConfig'];
            runCommand: string;
            region: components['schemas']['Region'];
        };
        WorkflowUpdate: {
            name?: string;
            buildConfig?: components['schemas']['BuildConfig'];
            runCommand?: string;
        };
        WorkflowVersionStatus: 'created' | 'building' | 'registering' | 'build_failed' | 'registration_failed' | 'ready';
        WorkflowVersion: {
            id: string;
            workflowId: string;
            name: string;
            createdAt: string;
            status: components['schemas']['WorkflowVersionStatus'];
        };
        CreateVersion: {
            workflowId: string;
            commit?: string;
        };
        Task: {
            id: string;
            name: string;
            createdAt: string;
            workflowId?: string;
            workflowVersionId?: string;
        };
        TaskRunStatus: 'pending' | 'running' | 'completed' | 'failed' | 'canceled';
        TaskRun: {
            id: string;
            taskId: string;
            status: components['schemas']['TaskRunStatus'];
            startedAt?: string;
            completedAt?: string;
            parentTaskRunId: string;
            rootTaskRunId: string;
            retries: number;
        };
        TaskIdentifier: string;
        TaskData: unknown[];
        RunTask: {
            task: components['schemas']['TaskIdentifier'];
            input: components['schemas']['TaskData'];
        };
        TaskRunResult: unknown[];
        TaskRunDetails: {
            id: string;
            taskId: string;
            status: components['schemas']['TaskRunStatus'];
            results: components['schemas']['TaskRunResult'];
            error?: string;
            startedAt?: string;
            completedAt?: string;
            input: components['schemas']['TaskData'];
            parentTaskRunId: string;
            rootTaskRunId: string;
            retries: number;
        };
    };
    responses: {
        '400BadRequest': {
            headers: {
                [name: string]: unknown;
            };
            content: {
                'application/json': components['schemas']['error'];
            };
        };
        '401Unauthorized': {
            headers: {
                [name: string]: unknown;
            };
            content: {
                'application/json': components['schemas']['error'];
            };
        };
        '402PaymentRequired': {
            headers: {
                [name: string]: unknown;
            };
            content: {
                'application/json': components['schemas']['error'];
            };
        };
        '403Forbidden': {
            headers: {
                [name: string]: unknown;
            };
            content: {
                'application/json': components['schemas']['error'];
            };
        };
        '404NotFound': {
            headers: {
                [name: string]: unknown;
            };
            content: {
                'application/json': components['schemas']['error'];
            };
        };
        '406NotAcceptable': {
            headers: {
                [name: string]: unknown;
            };
            content: {
                'application/json': components['schemas']['error'];
            };
        };
        '409Conflict': {
            headers: {
                [name: string]: unknown;
            };
            content: {
                'application/json': components['schemas']['error'];
            };
        };
        '410Gone': {
            headers: {
                [name: string]: unknown;
            };
            content: {
                'application/json': components['schemas']['error'];
            };
        };
        '429RateLimit': {
            headers: {
                [name: string]: unknown;
            };
            content: {
                'application/json': components['schemas']['error'];
            };
        };
        '500InternalServerError': {
            headers: {
                [name: string]: unknown;
            };
            content: {
                'application/json': components['schemas']['error'];
            };
        };
        '503ServiceUnavailable': {
            headers: {
                [name: string]: unknown;
            };
            content: {
                'application/json': components['schemas']['error'];
            };
        };
        Logs200Response: {
            headers: {
                [name: string]: unknown;
            };
            content: {
                'application/json': {
                    hasMore: boolean;
                    nextStartTime: string;
                    nextEndTime: string;
                    logs: components['schemas']['log'][];
                };
            };
        };
        LogsValues200Response: {
            headers: {
                [name: string]: unknown;
            };
            content: {
                'application/json': string[];
            };
        };
        GetOwnerLogsStreams200Response: {
            headers: {
                [name: string]: unknown;
            };
            content: {
                'application/json': components['schemas']['ownerLogStreamSetting'];
            };
        };
        ResourceLogsStreams200Response: {
            headers: {
                [name: string]: unknown;
            };
            content: {
                'application/json': components['schemas']['resourceLogStreamSetting'][];
            };
        };
        GetResourceLogsStreams200Response: {
            headers: {
                [name: string]: unknown;
            };
            content: {
                'application/json': components['schemas']['resourceLogStreamSetting'];
            };
        };
        GetMetricsStream200Response: {
            headers: {
                [name: string]: unknown;
            };
            content: {
                'application/json': components['schemas']['metricsStream'];
            };
        };
        Metrics200Response: {
            headers: {
                [name: string]: unknown;
            };
            content: {
                'application/json': components['schemas']['timeSeriesCollection'];
            };
        };
        MetricsFiltersApplication200Response: {
            headers: {
                [name: string]: unknown;
            };
            content: {
                'application/json': components['schemas']['filterApplicationValuesCollection'];
            };
        };
        MetricsFiltersHTTP200Response: {
            headers: {
                [name: string]: unknown;
            };
            content: {
                'application/json': components['schemas']['filterHTTPValuesCollection'];
            };
        };
        MetricsFiltersPath200Response: {
            headers: {
                [name: string]: unknown;
            };
            content: {
                'application/json': components['schemas']['filterPathValuesCollection'];
            };
        };
    };
    parameters: {
        cursorParam: string;
        customDomainIdOrNameParam: string;
        deployIdParam: string;
        limitParam: number;
        auditLogLimitParam: number;
        ownerIdPathParam: string;
        ownerIdParam: string[];
        workflowIdParam: string[];
        workflowVersionIdParam: string[];
        resourceIdParam: string[];
        serviceIdParam: string;
        cronJobIdParam: string;
        serviceIdsParam: string[];
        startTimeParam: string;
        endTimeParam: string;
        nameParam: string[];
        serviceTypeParam: components['schemas']['serviceType'][];
        envParam: components['schemas']['serviceRuntime'][];
        runtimeParam: components['schemas']['serviceRuntime'][];
        regionParam: components['schemas']['region'][];
        suspendedParam: ('suspended' | 'not_suspended')[];
        createdBeforeParam: string;
        createdAfterParam: string;
        updatedBeforeParam: string;
        updatedAfterParam: string;
        projectIdParam: string[];
        environmentIdParam: string[];
        includePreviewsParam: boolean;
        includeReplicasParam: boolean;
        envGroupIdParam: string;
        envVarKeyParam: string;
        secretFileNameParam: string;
        eventTypeParam: components['schemas']['serviceEventType'];
        blueprintId: components['schemas']['blueprintId'];
        diskIdQuery: components['schemas']['diskId'][];
        diskId: components['schemas']['diskId'];
        jobId: components['schemas']['jobId'];
        logDirectionParam: components['schemas']['logDirection'];
        logFilterResource: string[];
        logFilterInstance: string[];
        logFilterHost: string[];
        logFilterStatusCode: string[];
        logFilterMethod: string[];
        logFilterTask: string[];
        logFilterTaskRun: string[];
        logFilterLevel: string[];
        logFilterType: string[];
        logFilterText: string[];
        logFilterPath: string[];
        logLabelParam: 'instance' | 'host' | 'statusCode' | 'method' | 'level' | 'type';
        logStreamIdFilter: string[];
        logStreamSettingFilter: components['schemas']['logStreamSetting'][];
        resolutionParam: number;
        resourceQueryParam: string;
        serviceQueryParam: string;
        instanceQueryParam: string;
        applicationMetricAggregationMethod: 'AVG' | 'MAX' | 'MIN';
        serviceResourceQueryParam: string;
        hostQueryParam: string;
        pathQueryParam: string;
        httpAggregateBy: 'statusCode' | 'host';
        quantile: number;
        datastoreResourceQueryParam: string;
        postgresResourceQueryParam: string;
        httpStatusCode: string;
        maintenanceResourcesParam: components['schemas']['maintenanceResourceId'][];
        maintenanceStateParam: components['schemas']['maintenanceState'][];
        maintenanceRunParam: components['schemas']['maintenanceRunId'];
        webhookIdParam: components['schemas']['webhookId'];
        sentBeforeParam: string;
        sentAfterParam: string;
        WorkflowIDParam: string;
        WorkflowVersionIDParam: string;
        TaskIdFilterParam: string[];
        WorkflowVersionIDFilterParam: string[];
        WorkflowIDFilterParam: string[];
        TaskIDParam: string;
        RootTaskRunIDFilterParam: string[];
        TaskRunIDParam: string;
    };
    requestBodies: never;
    headers: never;
    pathItems: never;
}
export type $defs = Record<string, never>;
export interface operations {
    'list-blueprints': {
        parameters: {
            query?: {
                ownerId?: components['parameters']['ownerIdParam'];
                cursor?: components['parameters']['cursorParam'];
                limit?: components['parameters']['limitParam'];
            };
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
                    'application/json': components['schemas']['blueprintWithCursor'][];
                };
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'retrieve-blueprint': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                blueprintId: components['parameters']['blueprintId'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['blueprintDetail'];
                };
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'disconnect-blueprint': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                blueprintId: components['parameters']['blueprintId'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'update-blueprint': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                blueprintId: components['parameters']['blueprintId'];
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['blueprintPATCH'];
            };
        };
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['blueprint'];
                };
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'list-blueprint-syncs': {
        parameters: {
            query?: {
                cursor?: components['parameters']['cursorParam'];
                limit?: components['parameters']['limitParam'];
            };
            header?: never;
            path: {
                blueprintId: components['parameters']['blueprintId'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['syncWithCursor'][];
                };
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'list-disks': {
        parameters: {
            query?: {
                ownerId?: components['parameters']['ownerIdParam'];
                diskId?: components['parameters']['diskIdQuery'];
                name?: components['parameters']['nameParam'];
                createdBefore?: components['parameters']['createdBeforeParam'];
                createdAfter?: components['parameters']['createdAfterParam'];
                updatedBefore?: components['parameters']['updatedBeforeParam'];
                updatedAfter?: components['parameters']['updatedAfterParam'];
                serviceId?: components['parameters']['serviceIdsParam'];
                cursor?: components['parameters']['cursorParam'];
                limit?: components['parameters']['limitParam'];
            };
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
                    'application/json': components['schemas']['diskWithCursor'][];
                };
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'add-disk': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['diskPOST'];
            };
        };
        responses: {
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['diskDetails'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'retrieve-disk': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                diskId: components['parameters']['diskId'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['diskDetails'];
                };
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'delete-disk': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                diskId: components['parameters']['diskId'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'update-disk': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                diskId: components['parameters']['diskId'];
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['diskPATCH'];
            };
        };
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['diskDetails'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'list-snapshots': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                diskId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['diskSnapshot'][];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'restore-snapshot': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                diskId: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['snapshotRestorePOST'];
            };
        };
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['diskDetails'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'get-user': {
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
                    'application/json': components['schemas']['user'];
                };
            };
            401: components['responses']['401Unauthorized'];
            406: components['responses']['406NotAcceptable'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'list-owners': {
        parameters: {
            query?: {
                name?: string[];
                email?: string[];
                cursor?: components['parameters']['cursorParam'];
                limit?: components['parameters']['limitParam'];
            };
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
                    'application/json': components['schemas']['ownerWithCursor'][];
                };
            };
            401: components['responses']['401Unauthorized'];
            406: components['responses']['406NotAcceptable'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'retrieve-owner': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                ownerId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['owner'];
                };
            };
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'retrieve-owner-members': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                ownerId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['teamMembers'];
                };
            };
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'list-owner-audit-logs': {
        parameters: {
            query?: {
                startTime?: string;
                endTime?: string;
                cursor?: components['parameters']['cursorParam'];
                limit?: components['parameters']['auditLogLimitParam'];
            };
            header?: never;
            path: {
                ownerId: components['parameters']['ownerIdPathParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['auditLogWithCursor'][];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'list-organization-audit-logs': {
        parameters: {
            query?: {
                startTime?: string;
                endTime?: string;
                cursor?: components['parameters']['cursorParam'];
                limit?: components['parameters']['auditLogLimitParam'];
            };
            header?: never;
            path: {
                orgId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['auditLogWithCursor'][];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'retrieve-owner-notification-settings': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                ownerId: components['parameters']['ownerIdPathParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['notificationSetting'];
                };
            };
            401: components['responses']['401Unauthorized'];
            406: components['responses']['406NotAcceptable'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'patch-owner-notification-settings': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                ownerId: components['parameters']['ownerIdPathParam'];
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['notificationSettingPATCH'];
            };
        };
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['notificationSetting'];
                };
            };
            401: components['responses']['401Unauthorized'];
            406: components['responses']['406NotAcceptable'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'list-notification-overrides': {
        parameters: {
            query?: {
                ownerId?: components['parameters']['ownerIdParam'];
                serviceId?: components['parameters']['serviceIdsParam'];
                cursor?: components['parameters']['cursorParam'];
                limit?: components['parameters']['limitParam'];
            };
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
                    'application/json': components['schemas']['notificationOverrideWithCursor'][];
                };
            };
            401: components['responses']['401Unauthorized'];
            406: components['responses']['406NotAcceptable'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'retrieve-service-notification-overrides': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['notificationServiceOverride'];
                };
            };
            401: components['responses']['401Unauthorized'];
            406: components['responses']['406NotAcceptable'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'patch-service-notification-overrides': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['notificationServiceOverridePATCH'];
            };
        };
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['notificationServiceOverride'];
                };
            };
            401: components['responses']['401Unauthorized'];
            406: components['responses']['406NotAcceptable'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'list-registry-credentials': {
        parameters: {
            query?: {
                name?: string[];
                username?: string[];
                type?: components['schemas']['registryCredentialRegistry'][];
                createdBefore?: string;
                createdAfter?: string;
                updatedBefore?: string;
                updatedAfter?: string;
                ownerId?: components['parameters']['ownerIdParam'];
                cursor?: components['parameters']['cursorParam'];
                limit?: components['parameters']['limitParam'];
            };
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
                    'application/json': components['schemas']['registryCredential'][];
                };
            };
            401: components['responses']['401Unauthorized'];
            406: components['responses']['406NotAcceptable'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'create-registry-credential': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': {
                    registry: components['schemas']['registryCredentialRegistry'];
                    name: string;
                    username: string;
                    authToken: string;
                    ownerId: string;
                };
            };
        };
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['registryCredential'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            402: components['responses']['402PaymentRequired'];
            406: components['responses']['406NotAcceptable'];
            409: components['responses']['409Conflict'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'retrieve-registry-credential': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                registryCredentialId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['registryCredential'];
                };
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'delete-registry-credential': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                registryCredentialId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'update-registry-credential': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                registryCredentialId: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': {
                    registry: components['schemas']['registryCredentialRegistry'];
                    name: string;
                    username: string;
                    authToken: string;
                };
            };
        };
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['registryCredential'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            402: components['responses']['402PaymentRequired'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            409: components['responses']['409Conflict'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'list-services': {
        parameters: {
            query?: {
                name?: components['parameters']['nameParam'];
                type?: components['parameters']['serviceTypeParam'];
                environmentId?: components['parameters']['environmentIdParam'];
                env?: components['parameters']['envParam'];
                region?: components['parameters']['regionParam'];
                suspended?: components['parameters']['suspendedParam'];
                createdBefore?: components['parameters']['createdBeforeParam'];
                createdAfter?: components['parameters']['createdAfterParam'];
                updatedBefore?: components['parameters']['updatedBeforeParam'];
                updatedAfter?: components['parameters']['updatedAfterParam'];
                ownerId?: components['parameters']['ownerIdParam'];
                includePreviews?: components['parameters']['includePreviewsParam'];
                cursor?: components['parameters']['cursorParam'];
                limit?: components['parameters']['limitParam'];
            };
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
                    'application/json': components['schemas']['serviceList'];
                };
            };
            401: components['responses']['401Unauthorized'];
            406: components['responses']['406NotAcceptable'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'create-service': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['servicePOST'];
            };
        };
        responses: {
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['serviceAndDeploy'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            402: components['responses']['402PaymentRequired'];
            406: components['responses']['406NotAcceptable'];
            409: components['responses']['409Conflict'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'retrieve-service': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['service'];
                };
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'delete-service': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'update-service': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['servicePATCH'];
            };
        };
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['service'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            402: components['responses']['402PaymentRequired'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            409: components['responses']['409Conflict'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'purge-cache': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody?: {
            content: {
                '*/*'?: never;
            };
        };
        responses: {
            202: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            409: components['responses']['409Conflict'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'list-deploys': {
        parameters: {
            query?: {
                status?: components['schemas']['deployStatus'][];
                createdBefore?: string;
                createdAfter?: string;
                updatedBefore?: string;
                updatedAfter?: string;
                finishedBefore?: string;
                finishedAfter?: string;
                cursor?: components['parameters']['cursorParam'];
                limit?: components['parameters']['limitParam'];
            };
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['deployList'];
                };
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'create-deploy': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': {
                    clearCache?: 'clear' | 'do_not_clear';
                    commitId?: string;
                    imageUrl?: string;
                };
            };
        };
        responses: {
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['deploy'];
                };
            };
            202: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            409: components['responses']['409Conflict'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'retrieve-deploy': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
                deployId: components['parameters']['deployIdParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['deploy'];
                };
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'cancel-deploy': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
                deployId: components['parameters']['deployIdParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['deploy'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'rollback-deploy': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': {
                    deployId: string;
                };
            };
        };
        responses: {
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['deploy'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'get-env-vars-for-service': {
        parameters: {
            query?: {
                cursor?: components['parameters']['cursorParam'];
                limit?: components['parameters']['limitParam'];
            };
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['envVarWithCursor'][];
                };
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'update-env-vars-for-service': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['envVarInputArray'];
            };
        };
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['envVarWithCursor'][];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'retrieve-env-var': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
                envVarKey: components['parameters']['envVarKeyParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['envVar'];
                };
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'update-env-var': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
                envVarKey: components['parameters']['envVarKeyParam'];
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['addUpdateEnvVarInput'];
            };
        };
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['envVar'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'delete-env-var': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
                envVarKey: components['parameters']['envVarKeyParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'list-secret-files-for-service': {
        parameters: {
            query?: {
                cursor?: components['parameters']['cursorParam'];
                limit?: components['parameters']['limitParam'];
            };
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['secretFileWithCursor'][];
                };
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'update-secret-files-for-service': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['secretFileInput'][];
            };
        };
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['secretFileWithCursor'][];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'retrieve-secret-file': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
                secretFileName: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['secretFile'];
                };
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'add-or-update-secret-file': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
                secretFileName: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': {
                    content?: string;
                };
            };
        };
        responses: {
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['secretFile'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'delete-secret-file': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
                secretFileName: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'list-events': {
        parameters: {
            query?: {
                type?: components['parameters']['eventTypeParam'];
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                cursor?: components['parameters']['cursorParam'];
                limit?: components['parameters']['limitParam'];
            };
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['serviceEventWithCursor'][];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'list-headers': {
        parameters: {
            query?: {
                path?: string[];
                name?: string[];
                value?: string[];
                cursor?: components['parameters']['cursorParam'];
                limit?: components['parameters']['limitParam'];
            };
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['headerWithCursor'][];
                };
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'update-headers': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['headerInput'][];
            };
        };
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['header'][];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'add-headers': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['headerInput'];
            };
        };
        responses: {
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': {
                        headers?: components['schemas']['header'];
                    };
                };
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'delete-header': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
                headerId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'list-routes': {
        parameters: {
            query?: {
                type?: ('redirect' | 'rewrite')[];
                source?: string[];
                destination?: string[];
                cursor?: components['parameters']['cursorParam'];
                limit?: components['parameters']['limitParam'];
            };
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['routeWithCursor'][];
                };
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'put-routes': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['routePut'][];
            };
        };
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['route'][];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'add-route': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['routePost'];
            };
        };
        responses: {
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['route'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'patch-route': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['routePatch'];
            };
        };
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': {
                        headers?: components['schemas']['route'];
                    };
                };
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'delete-route': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
                routeId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'list-custom-domains': {
        parameters: {
            query?: {
                cursor?: components['parameters']['cursorParam'];
                limit?: components['parameters']['limitParam'];
                name?: string[];
                domainType?: 'apex' | 'subdomain';
                verificationStatus?: 'verified' | 'unverified';
                createdBefore?: string;
                createdAfter?: string;
            };
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['customDomainWithCursor'][];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'create-custom-domain': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': {
                    name: string;
                };
            };
        };
        responses: {
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['customDomain'][];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            402: components['responses']['402PaymentRequired'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            409: components['responses']['409Conflict'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'retrieve-custom-domain': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
                customDomainIdOrName: components['parameters']['customDomainIdOrNameParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['customDomain'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'delete-custom-domain': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
                customDomainIdOrName: components['parameters']['customDomainIdOrNameParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'refresh-custom-domain': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
                customDomainIdOrName: components['parameters']['customDomainIdOrNameParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            202: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'suspend-service': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            202: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'resume-service': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            202: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'restart-service': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'scale-service': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': {
                    numInstances: number;
                };
            };
        };
        responses: {
            202: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'autoscale-service': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['autoscalingConfig'];
            };
        };
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['autoscalingConfig'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'delete-autoscaling-config': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'preview-service': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['previewInput'];
            };
        };
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['serviceAndDeploy'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'list-job': {
        parameters: {
            query?: {
                cursor?: components['parameters']['cursorParam'];
                limit?: components['parameters']['limitParam'];
                status?: components['schemas']['jobStatus'][];
                createdBefore?: string;
                createdAfter?: string;
                startedBefore?: string;
                startedAfter?: string;
                finishedBefore?: string;
                finishedAfter?: string;
            };
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['jobWithCursor'][];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'post-job': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': {
                    startCommand: string;
                    planId?: string;
                };
            };
        };
        responses: {
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['job'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'retrieve-job': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
                jobId: components['parameters']['jobId'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['job'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'cancel-job': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
                jobId: components['parameters']['jobId'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['job'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'list-instances': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['serviceInstance'][];
                };
            };
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'run-cron-job': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                cronJobId: components['parameters']['cronJobIdParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['cronJobRun'];
                };
            };
            401: components['responses']['401Unauthorized'];
            406: components['responses']['406NotAcceptable'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'cancel-cron-job-run': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                cronJobId: components['parameters']['cronJobIdParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            401: components['responses']['401Unauthorized'];
            406: components['responses']['406NotAcceptable'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'retrieve-event': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                eventId: components['schemas']['eventId'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['event'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'list-logs': {
        parameters: {
            query: {
                ownerId: string;
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                direction?: components['parameters']['logDirectionParam'];
                resource: components['parameters']['logFilterResource'];
                instance?: components['parameters']['logFilterInstance'];
                host?: components['parameters']['logFilterHost'];
                statusCode?: components['parameters']['logFilterStatusCode'];
                method?: components['parameters']['logFilterMethod'];
                task?: components['parameters']['logFilterTask'];
                taskRun?: components['parameters']['logFilterTaskRun'];
                level?: components['parameters']['logFilterLevel'];
                type?: components['parameters']['logFilterType'];
                text?: components['parameters']['logFilterText'];
                path?: components['parameters']['logFilterPath'];
                limit?: components['parameters']['limitParam'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: components['responses']['Logs200Response'];
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'subscribe-logs': {
        parameters: {
            query: {
                ownerId: string;
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                direction?: components['parameters']['logDirectionParam'];
                resource: components['parameters']['logFilterResource'];
                instance?: components['parameters']['logFilterInstance'];
                host?: components['parameters']['logFilterHost'];
                statusCode?: components['parameters']['logFilterStatusCode'];
                method?: components['parameters']['logFilterMethod'];
                task?: components['parameters']['logFilterTask'];
                taskRun?: components['parameters']['logFilterTaskRun'];
                level?: components['parameters']['logFilterLevel'];
                type?: components['parameters']['logFilterType'];
                text?: components['parameters']['logFilterText'];
                path?: components['parameters']['logFilterPath'];
                limit?: components['parameters']['limitParam'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            101: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['log'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'list-logs-values': {
        parameters: {
            query: {
                ownerId: string;
                label: components['parameters']['logLabelParam'];
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                direction?: components['parameters']['logDirectionParam'];
                resource: components['parameters']['logFilterResource'];
                instance?: components['parameters']['logFilterInstance'];
                host?: components['parameters']['logFilterHost'];
                statusCode?: components['parameters']['logFilterStatusCode'];
                method?: components['parameters']['logFilterMethod'];
                task?: components['parameters']['logFilterTask'];
                taskRun?: components['parameters']['logFilterTaskRun'];
                level?: components['parameters']['logFilterLevel'];
                type?: components['parameters']['logFilterType'];
                text?: components['parameters']['logFilterText'];
                path?: components['parameters']['logFilterPath'];
                limit?: components['parameters']['limitParam'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: components['responses']['LogsValues200Response'];
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'get-owner-log-stream': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                ownerId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: components['responses']['GetOwnerLogsStreams200Response'];
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'update-owner-log-stream': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                ownerId: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['logStreamOwnerUpdate'];
            };
        };
        responses: {
            200: components['responses']['GetOwnerLogsStreams200Response'];
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'delete-owner-log-stream': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                ownerId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'list-resource-log-streams': {
        parameters: {
            query?: {
                ownerId?: components['parameters']['ownerIdParam'];
                logStreamId?: components['parameters']['logStreamIdFilter'];
                resourceId?: components['parameters']['resourceIdParam'];
                setting?: components['parameters']['logStreamSettingFilter'];
                cursor?: components['parameters']['cursorParam'];
                limit?: components['parameters']['limitParam'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: components['responses']['ResourceLogsStreams200Response'];
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'get-resource-log-stream': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                resourceId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: components['responses']['GetResourceLogsStreams200Response'];
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'update-resource-log-stream': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                resourceId: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['logStreamResourceUpdate'];
            };
        };
        responses: {
            200: components['responses']['GetResourceLogsStreams200Response'];
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'delete-resource-log-stream': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                resourceId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    getOwnerMetricsStream: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                ownerId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: components['responses']['GetMetricsStream200Response'];
            400: components['responses']['400BadRequest'];
            404: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            500: components['responses']['500InternalServerError'];
        };
    };
    upsertOwnerMetricsStream: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                ownerId: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['metricsStreamInput'];
            };
        };
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['metricsStream'];
                };
            };
            400: components['responses']['400BadRequest'];
            500: components['responses']['500InternalServerError'];
        };
    };
    deleteOwnerMetricsStream: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                ownerId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            400: components['responses']['400BadRequest'];
            404: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            500: components['responses']['500InternalServerError'];
        };
    };
    'get-cpu': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resolutionSeconds?: components['parameters']['resolutionParam'];
                resource?: components['parameters']['resourceQueryParam'];
                service?: components['parameters']['serviceQueryParam'];
                instance?: components['parameters']['instanceQueryParam'];
                aggregationMethod?: components['parameters']['applicationMetricAggregationMethod'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: components['responses']['Metrics200Response'];
            400: components['responses']['400BadRequest'];
            500: components['responses']['500InternalServerError'];
        };
    };
    'get-cpu-limit': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resolutionSeconds?: components['parameters']['resolutionParam'];
                resource?: components['parameters']['resourceQueryParam'];
                service?: components['parameters']['serviceQueryParam'];
                instance?: components['parameters']['instanceQueryParam'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: components['responses']['Metrics200Response'];
            400: components['responses']['400BadRequest'];
            500: components['responses']['500InternalServerError'];
        };
    };
    'get-cpu-target': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resolutionSeconds?: components['parameters']['resolutionParam'];
                resource?: components['parameters']['resourceQueryParam'];
                service?: components['parameters']['serviceQueryParam'];
                instance?: components['parameters']['instanceQueryParam'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: components['responses']['Metrics200Response'];
            400: components['responses']['400BadRequest'];
            500: components['responses']['500InternalServerError'];
        };
    };
    'get-memory': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resolutionSeconds?: components['parameters']['resolutionParam'];
                resource?: components['parameters']['resourceQueryParam'];
                service?: components['parameters']['serviceQueryParam'];
                instance?: components['parameters']['instanceQueryParam'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: components['responses']['Metrics200Response'];
            400: components['responses']['400BadRequest'];
            500: components['responses']['500InternalServerError'];
        };
    };
    'get-memory-limit': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resolutionSeconds?: components['parameters']['resolutionParam'];
                resource?: components['parameters']['resourceQueryParam'];
                service?: components['parameters']['serviceQueryParam'];
                instance?: components['parameters']['instanceQueryParam'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: components['responses']['Metrics200Response'];
            400: components['responses']['400BadRequest'];
            500: components['responses']['500InternalServerError'];
        };
    };
    'get-memory-target': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resolutionSeconds?: components['parameters']['resolutionParam'];
                resource?: components['parameters']['resourceQueryParam'];
                service?: components['parameters']['serviceQueryParam'];
                instance?: components['parameters']['instanceQueryParam'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: components['responses']['Metrics200Response'];
            400: components['responses']['400BadRequest'];
            500: components['responses']['500InternalServerError'];
        };
    };
    'get-http-requests': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resolutionSeconds?: components['parameters']['resolutionParam'];
                resource?: components['parameters']['serviceResourceQueryParam'];
                service?: components['parameters']['serviceQueryParam'];
                host?: components['parameters']['hostQueryParam'];
                path?: components['parameters']['pathQueryParam'];
                aggregateBy?: components['parameters']['httpAggregateBy'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: components['responses']['Metrics200Response'];
            400: components['responses']['400BadRequest'];
            500: components['responses']['500InternalServerError'];
        };
    };
    'get-http-latency': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resolutionSeconds?: components['parameters']['resolutionParam'];
                resource?: components['parameters']['serviceResourceQueryParam'];
                service?: components['parameters']['serviceQueryParam'];
                host?: components['parameters']['hostQueryParam'];
                path?: components['parameters']['pathQueryParam'];
                quantile?: components['parameters']['quantile'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: components['responses']['Metrics200Response'];
            400: components['responses']['400BadRequest'];
            500: components['responses']['500InternalServerError'];
        };
    };
    'get-bandwidth': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resource?: components['parameters']['serviceResourceQueryParam'];
                service?: components['parameters']['serviceQueryParam'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: components['responses']['Metrics200Response'];
            400: components['responses']['400BadRequest'];
            500: components['responses']['500InternalServerError'];
        };
    };
    'get-bandwidth-sources': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resource?: components['parameters']['serviceResourceQueryParam'];
                service?: components['parameters']['serviceQueryParam'];
            };
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
                    'application/json': {
                        data?: {
                            labels?: {
                                resource?: string;
                                trafficSource?: 'total' | 'http' | 'websocket' | 'nat' | 'privatelink';
                            };
                            values?: {
                                timestamp?: number;
                                value?: number;
                            }[];
                        }[];
                    };
                };
            };
            400: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': {
                        error?: string;
                    };
                };
            };
            500: components['responses']['500InternalServerError'];
        };
    };
    'get-disk-usage': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resolutionSeconds?: components['parameters']['resolutionParam'];
                resource?: components['parameters']['resourceQueryParam'];
                service?: components['parameters']['serviceQueryParam'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: components['responses']['Metrics200Response'];
            400: components['responses']['400BadRequest'];
            500: components['responses']['500InternalServerError'];
        };
    };
    'get-disk-capacity': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resolutionSeconds?: components['parameters']['resolutionParam'];
                resource?: components['parameters']['resourceQueryParam'];
                service?: components['parameters']['serviceQueryParam'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: components['responses']['Metrics200Response'];
            400: components['responses']['400BadRequest'];
            500: components['responses']['500InternalServerError'];
        };
    };
    'get-instance-count': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resolutionSeconds?: components['parameters']['resolutionParam'];
                resource?: components['parameters']['resourceQueryParam'];
                service?: components['parameters']['serviceQueryParam'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: components['responses']['Metrics200Response'];
            400: components['responses']['400BadRequest'];
            500: components['responses']['500InternalServerError'];
        };
    };
    'get-active-connections': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resolutionSeconds?: components['parameters']['resolutionParam'];
                resource?: components['parameters']['datastoreResourceQueryParam'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: components['responses']['Metrics200Response'];
            400: components['responses']['400BadRequest'];
            500: components['responses']['500InternalServerError'];
        };
    };
    'get-replication-lag': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resolutionSeconds?: components['parameters']['resolutionParam'];
                resource?: components['parameters']['postgresResourceQueryParam'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: components['responses']['Metrics200Response'];
            400: components['responses']['400BadRequest'];
            500: components['responses']['500InternalServerError'];
        };
    };
    'list-application-filter-values': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resolutionSeconds?: components['parameters']['resolutionParam'];
                resource?: components['parameters']['serviceResourceQueryParam'];
                service?: components['parameters']['serviceQueryParam'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: components['responses']['MetricsFiltersApplication200Response'];
            400: components['responses']['400BadRequest'];
            500: components['responses']['500InternalServerError'];
        };
    };
    'list-http-filter-values': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resolutionSeconds?: components['parameters']['resolutionParam'];
                resource?: components['parameters']['serviceResourceQueryParam'];
                service?: components['parameters']['serviceQueryParam'];
                host?: components['parameters']['hostQueryParam'];
                statusCode?: components['parameters']['httpStatusCode'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: components['responses']['MetricsFiltersHTTP200Response'];
            400: components['responses']['400BadRequest'];
            500: components['responses']['500InternalServerError'];
        };
    };
    'list-path-filter-values': {
        parameters: {
            query?: {
                startTime?: components['parameters']['startTimeParam'];
                endTime?: components['parameters']['endTimeParam'];
                resolutionSeconds?: components['parameters']['resolutionParam'];
                resource?: components['parameters']['serviceResourceQueryParam'];
                service?: components['parameters']['serviceQueryParam'];
                host?: components['parameters']['hostQueryParam'];
                statusCode?: components['parameters']['httpStatusCode'];
                path?: components['parameters']['pathQueryParam'];
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: components['responses']['MetricsFiltersPath200Response'];
            400: components['responses']['400BadRequest'];
            500: components['responses']['500InternalServerError'];
        };
    };
    'list-key-value': {
        parameters: {
            query?: {
                name?: components['parameters']['nameParam'];
                region?: components['parameters']['regionParam'];
                createdBefore?: components['parameters']['createdBeforeParam'];
                createdAfter?: components['parameters']['createdAfterParam'];
                updatedBefore?: components['parameters']['updatedBeforeParam'];
                updatedAfter?: components['parameters']['updatedAfterParam'];
                ownerId?: components['parameters']['ownerIdParam'];
                environmentId?: components['parameters']['environmentIdParam'];
                cursor?: components['parameters']['cursorParam'];
                limit?: components['parameters']['limitParam'];
            };
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
                    'application/json': components['schemas']['keyValueWithCursor'][];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            409: components['responses']['409Conflict'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'create-key-value': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['keyValuePOSTInput'];
            };
        };
        responses: {
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['keyValueDetail'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'retrieve-key-value': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                keyValueId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['keyValueDetail'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'delete-key-value': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                keyValueId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'update-key-value': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                keyValueId: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['keyValuePATCHInput'];
            };
        };
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['keyValueDetail'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            409: components['responses']['409Conflict'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'retrieve-key-value-connection-info': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                keyValueId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['keyValueConnectionInfo'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'list-redis': {
        parameters: {
            query?: {
                name?: components['parameters']['nameParam'];
                region?: components['parameters']['regionParam'];
                createdBefore?: components['parameters']['createdBeforeParam'];
                createdAfter?: components['parameters']['createdAfterParam'];
                updatedBefore?: components['parameters']['updatedBeforeParam'];
                updatedAfter?: components['parameters']['updatedAfterParam'];
                ownerId?: components['parameters']['ownerIdParam'];
                environmentId?: components['parameters']['environmentIdParam'];
                cursor?: components['parameters']['cursorParam'];
                limit?: components['parameters']['limitParam'];
            };
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
                    'application/json': components['schemas']['redisWithCursor'][];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            409: components['responses']['409Conflict'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'create-redis': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['redisPOSTInput'];
            };
        };
        responses: {
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['redisDetail'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'retrieve-redis': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                redisId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['redisDetail'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'delete-redis': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                redisId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'update-redis': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                redisId: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['redisPATCHInput'];
            };
        };
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['redisDetail'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            409: components['responses']['409Conflict'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'retrieve-redis-connection-info': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                redisId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['redisConnectionInfo'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'list-postgres': {
        parameters: {
            query?: {
                name?: components['parameters']['nameParam'];
                region?: components['parameters']['regionParam'];
                suspended?: components['parameters']['suspendedParam'];
                createdBefore?: components['parameters']['createdBeforeParam'];
                createdAfter?: components['parameters']['createdAfterParam'];
                updatedBefore?: components['parameters']['updatedBeforeParam'];
                updatedAfter?: components['parameters']['updatedAfterParam'];
                ownerId?: components['parameters']['ownerIdParam'];
                environmentId?: components['parameters']['environmentIdParam'];
                includeReplicas?: components['parameters']['includeReplicasParam'];
                cursor?: components['parameters']['cursorParam'];
                limit?: components['parameters']['limitParam'];
            };
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
                    'application/json': components['schemas']['postgresWithCursor'][];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            409: components['responses']['409Conflict'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'create-postgres': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['postgresPOSTInput'];
            };
        };
        responses: {
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['postgresDetail'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'retrieve-postgres': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                postgresId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['postgresDetail'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'delete-postgres': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                postgresId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'update-postgres': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                postgresId: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['postgresPATCHInput'];
            };
        };
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['postgresDetail'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            409: components['responses']['409Conflict'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'retrieve-postgres-connection-info': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                postgresId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['postgresConnectionInfo'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'retrieve-postgres-recovery-info': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                postgresId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['recoveryInfo'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'recover-postgres': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                postgresId: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['recoveryInput'];
            };
        };
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['postgresDetail'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'suspend-postgres': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                postgresId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            202: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'resume-postgres': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                postgresId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            202: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'restart-postgres': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                postgresId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            202: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'failover-postgres': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                postgresId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            202: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'list-postgres-export': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                postgresId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['postgresExport'][];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'create-postgres-export': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                postgresId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            202: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            406: components['responses']['406NotAcceptable'];
            410: components['responses']['410Gone'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'list-projects': {
        parameters: {
            query?: {
                name?: components['parameters']['nameParam'];
                createdBefore?: components['parameters']['createdBeforeParam'];
                createdAfter?: components['parameters']['createdAfterParam'];
                updatedBefore?: components['parameters']['updatedBeforeParam'];
                updatedAfter?: components['parameters']['updatedAfterParam'];
                ownerId?: components['parameters']['ownerIdParam'];
                cursor?: components['parameters']['cursorParam'];
                limit?: components['parameters']['limitParam'];
            };
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
                    'application/json': components['schemas']['projectWithCursor'][];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'create-project': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['projectPOSTInput'];
            };
        };
        responses: {
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['project'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'retrieve-project': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                projectId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['project'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'delete-project': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                projectId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'update-project': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                projectId: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['projectPATCHInput'];
            };
        };
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['project'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'list-environments': {
        parameters: {
            query: {
                name?: components['parameters']['nameParam'];
                projectId: components['parameters']['projectIdParam'];
                createdBefore?: components['parameters']['createdBeforeParam'];
                createdAfter?: components['parameters']['createdAfterParam'];
                updatedBefore?: components['parameters']['updatedBeforeParam'];
                updatedAfter?: components['parameters']['updatedAfterParam'];
                ownerId?: components['parameters']['ownerIdParam'];
                environmentId?: components['parameters']['environmentIdParam'];
                cursor?: components['parameters']['cursorParam'];
                limit?: components['parameters']['limitParam'];
            };
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
                    'application/json': components['schemas']['environmentWithCursor'][];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'create-environment': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['environmentPOSTInput'];
            };
        };
        responses: {
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['environment'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'retrieve-environment': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                environmentId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['environment'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'delete-environment': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                environmentId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'update-environment': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                environmentId: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['environmentPATCHInput'];
            };
        };
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['environment'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'add-resources-to-environment': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                environmentId: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['environmentResourcesPOSTInput'];
            };
        };
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['environment'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'remove-resources-from-environment': {
        parameters: {
            query: {
                resourceIds: string[];
            };
            header?: never;
            path: {
                environmentId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'list-env-groups': {
        parameters: {
            query?: {
                name?: components['parameters']['nameParam'];
                createdBefore?: components['parameters']['createdBeforeParam'];
                createdAfter?: components['parameters']['createdAfterParam'];
                updatedBefore?: components['parameters']['updatedBeforeParam'];
                updatedAfter?: components['parameters']['updatedAfterParam'];
                ownerId?: components['parameters']['ownerIdParam'];
                environmentId?: components['parameters']['environmentIdParam'];
                cursor?: components['parameters']['cursorParam'];
                limit?: components['parameters']['limitParam'];
            };
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
                    'application/json': components['schemas']['envGroupMeta'][];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'create-env-group': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['envGroupPOSTInput'];
            };
        };
        responses: {
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['envGroup'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'retrieve-env-group': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                envGroupId: components['parameters']['envGroupIdParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['envGroup'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'delete-env-group': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                envGroupId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'update-env-group': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                envGroupId: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['envGroupPATCHInput'];
            };
        };
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['envGroup'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'link-service-to-env-group': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                envGroupId: components['parameters']['envGroupIdParam'];
                serviceId: components['parameters']['serviceIdParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['envGroup'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'unlink-service-from-env-group': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                envGroupId: string;
                serviceId: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'retrieve-env-group-env-var': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                envGroupId: components['parameters']['envGroupIdParam'];
                envVarKey: components['parameters']['envVarKeyParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['envVar'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'update-env-group-env-var': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                envGroupId: components['parameters']['envGroupIdParam'];
                envVarKey: components['parameters']['envVarKeyParam'];
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['addUpdateEnvVarInput'];
            };
        };
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['envGroup'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'delete-env-group-env-var': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                envGroupId: string;
                envVarKey: components['parameters']['envVarKeyParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'retrieve-env-group-secret-file': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                envGroupId: components['parameters']['envGroupIdParam'];
                secretFileName: components['parameters']['secretFileNameParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['secretFile'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'update-env-group-secret-file': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                envGroupId: string;
                secretFileName: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': {
                    content?: string;
                };
            };
        };
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['envGroup'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'delete-env-group-secret-file': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                envGroupId: components['parameters']['envGroupIdParam'];
                secretFileName: components['parameters']['secretFileNameParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'list-maintenance': {
        parameters: {
            query?: {
                resourceId?: components['parameters']['maintenanceResourcesParam'];
                ownerId?: components['parameters']['ownerIdParam'];
                state?: components['parameters']['maintenanceStateParam'];
            };
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
                    'application/json': components['schemas']['maintenanceRunWithResource'][];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'retrieve-maintenance': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                maintenanceRunParam: components['parameters']['maintenanceRunParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['maintenanceRunWithResource'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'update-maintenance': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                maintenanceRunParam: components['parameters']['maintenanceRunParam'];
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['maintenanceRunPATCH'];
            };
        };
        responses: {
            202: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'trigger-maintenance': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                maintenanceRunParam: components['parameters']['maintenanceRunParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            202: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'list-webhooks': {
        parameters: {
            query?: {
                cursor?: components['parameters']['cursorParam'];
                limit?: components['parameters']['limitParam'];
                ownerId?: components['parameters']['ownerIdParam'];
            };
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
                    'application/json': components['schemas']['webhookWithCursor'][];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'create-webhook': {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['webhookPOSTInput'];
            };
        };
        responses: {
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['webhook'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'retrieve-webhook': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                webhookId: components['parameters']['webhookIdParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['webhook'];
                };
            };
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'delete-webhook': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                webhookId: components['parameters']['webhookIdParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'update-webhook': {
        parameters: {
            query?: never;
            header?: never;
            path: {
                webhookId: components['parameters']['webhookIdParam'];
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['webhookPATCHInput'];
            };
        };
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['webhook'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    'list-webhook-events': {
        parameters: {
            query?: {
                sentBefore?: components['parameters']['sentBeforeParam'];
                sentAfter?: components['parameters']['sentAfterParam'];
                limit?: components['parameters']['limitParam'];
                cursor?: components['parameters']['cursorParam'];
            };
            header?: never;
            path: {
                webhookId: components['parameters']['webhookIdParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['webhookEventWithCursor'][];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    listWorkflows: {
        parameters: {
            query?: {
                name?: components['parameters']['nameParam'];
                ownerId?: components['parameters']['ownerIdParam'];
                workflowID?: components['parameters']['workflowIdParam'];
                environmentId?: components['parameters']['environmentIdParam'];
                cursor?: components['parameters']['cursorParam'];
                limit?: components['parameters']['limitParam'];
            };
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
                    'application/json': components['schemas']['workflowWithCursor'][];
                };
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    createWorkflow: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['WorkflowCreate'];
            };
        };
        responses: {
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['Workflow'];
                };
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    getWorkflow: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                workflowId: components['parameters']['WorkflowIDParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['Workflow'];
                };
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    deleteWorkflow: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                workflowId: components['parameters']['WorkflowIDParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    updateWorkflow: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                workflowId: components['parameters']['WorkflowIDParam'];
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['WorkflowUpdate'];
            };
        };
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['Workflow'];
                };
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    listWorkflowVersions: {
        parameters: {
            query?: {
                ownerId?: components['parameters']['ownerIdParam'];
                workflowID?: components['parameters']['workflowIdParam'];
                workflowVersionId?: components['parameters']['workflowVersionIdParam'];
                cursor?: components['parameters']['cursorParam'];
                limit?: components['parameters']['limitParam'];
            };
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
                    'application/json': components['schemas']['workflowVersionWithCursor'][];
                };
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    createWorkflowVersion: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['CreateVersion'];
            };
        };
        responses: {
            202: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    getWorkflowVersion: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                workflowVersionId: components['parameters']['WorkflowVersionIDParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['WorkflowVersion'];
                };
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    listTasks: {
        parameters: {
            query?: {
                ownerId?: components['parameters']['ownerIdParam'];
                taskId?: components['parameters']['TaskIdFilterParam'];
                workflowVersionId?: components['parameters']['WorkflowVersionIDFilterParam'];
                workflowId?: components['parameters']['WorkflowIDFilterParam'];
                cursor?: components['parameters']['cursorParam'];
                limit?: components['parameters']['limitParam'];
            };
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
                    'application/json': components['schemas']['taskWithCursor'][];
                };
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    getTask: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                taskId: components['parameters']['TaskIDParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['Task'];
                };
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    listTaskRuns: {
        parameters: {
            query?: {
                cursor?: components['parameters']['cursorParam'];
                limit?: components['parameters']['limitParam'];
                taskId?: components['parameters']['TaskIdFilterParam'];
                rootTaskRunId?: components['parameters']['RootTaskRunIDFilterParam'];
                ownerId?: components['parameters']['ownerIdParam'];
                workflowVersionId?: components['parameters']['WorkflowVersionIDFilterParam'];
                workflowId?: components['parameters']['WorkflowIDFilterParam'];
            };
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
                    'application/json': components['schemas']['TaskRun'][];
                };
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    createTask: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                'application/json': components['schemas']['RunTask'];
            };
        };
        responses: {
            202: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['TaskRun'];
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    streamTaskRunsEvents: {
        parameters: {
            query: {
                taskRunIds: string[];
            };
            header?: {
                Accept?: 'text/event-stream';
            };
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    'Content-Type'?: string;
                    'Cache-Control'?: string;
                    Connection?: string;
                    [name: string]: unknown;
                };
                content: {
                    'text/event-stream': string;
                };
            };
            400: components['responses']['400BadRequest'];
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    getTaskRun: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                taskRunId: components['parameters']['TaskRunIDParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    'application/json': components['schemas']['TaskRunDetails'];
                };
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
    cancelTaskRun: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                taskRunId: components['parameters']['TaskRunIDParam'];
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
            401: components['responses']['401Unauthorized'];
            403: components['responses']['403Forbidden'];
            404: components['responses']['404NotFound'];
            429: components['responses']['429RateLimit'];
            500: components['responses']['500InternalServerError'];
            503: components['responses']['503ServiceUnavailable'];
        };
    };
}
//# sourceMappingURL=schema.d.ts.map