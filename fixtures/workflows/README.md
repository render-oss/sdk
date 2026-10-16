# Workflow golden fixtures

Language-neutral test cases for the durability rules that every workflows SDK
must follow: numbering steps, recording inline steps and their retries,
replaying against history, raising determinism errors, and handling the socket's
step routes. Each language implementation runs every case in this directory
through a small harness of its own. The cases describe what crosses the Unix
socket, so two SDKs that pass them behave the same way toward renderd.

The cases cover sequential inline steps. Detached tasks (`/run-subtask`,
`/step-wait`) and `ctx.sleep` (`/step-sleep`) have no cases. Steps are keyed by
a `step_key` object holding `seq`, and a failed attempt records `ended_at`.

`check.py` validates the cases' structure. It runs in CI and needs only the
Python standard library:

```sh
python3 fixtures/workflows/check.py
```

## Running a case

A harness runs one case as one workflow attempt:

1. Register a workflow whose body is the case's `workflow` program (see
   [Programs](#programs)).
2. Serve the socket API on a fake server. `GET /input` answers with
   `is_workflow: true`, `attempt` and `history` from the case, and an empty
   argument list (`[]`) as the workflow's input. Fill in the run ids however the
   harness likes.
3. Answer each step-route request with the next entry in `exchanges`, after
   checking that the request matches it (see [Matching](#matching)).
4. Once the attempt ends, check its outcome against `callback`.

A harness drives the SDK at the layer that returns when an attempt ends, below
any loop that waits for the process to be stopped. The attempt has ended when
that layer returns or throws. For `callback: null`, it returns without having
sent a callback.

The case fails if the SDK makes a step-route request that isn't the next
exchange, leaves an exchange unused, calls a step function more or fewer times
than its `attempts` list, or ends the attempt with a different callback.

Timing isn't part of a case. Every retry policy uses `wait_duration_ms: 0`, so
no attempt waits on a backoff. A harness may stub the SDK's sleeps, such as the
delay between socket retries.

## Known failures

An SDK that can't pass a case lists it rather than skipping it, so CI passes on
the known gaps and still catches new ones. Each harness keeps its own list, next
to the harness, as a JSON object from case name (the file name without `.json`)
to a reason that makes sense on its own, plus the ticket that fixes it:

```json
{
  "replay-memoized-output": "reads history with idx and failed_at (WOR-1797)"
}
```

The harness:

- runs every case, listed or not, so a listed case that crashes or hangs still
  shows up;
- fails when an unlisted case fails;
- fails when a listed case passes, so the entry comes off the list in the change
  that fixes it;
- fails when an entry names a case that doesn't exist.

To get a case passing, fix the SDK or list the case. Don't edit a case to match
one SDK: a case changes only when the contract does.

## Case format

Each case is one JSON file:

| Field | Meaning |
|---|---|
| `description` | The rule the case checks, in a sentence or two. |
| `attempt` | The workflow attempt number served on `/input`. 0 is the run's first attempt. |
| `history` | The history served on `/input`: `steps` and `step_attempts`. Absent when `attempt` is 0. |
| `workflow` | The workflow program: the `ctx` calls it makes, in order. |
| `exchanges` | Every step-route request the SDK must make, in order, and the response to each. |
| `callback` | The `/callback` the attempt must end with, or `null` for none. |

### Payloads

Every payload names its serializer. A payload is written as an object:

```json
{ "serializer": "json", "value": [100] }
```

`value` is the JSON document the payload carries. On the wire it is the base64
of that document, encoded as JSON. `json` is the only serializer. As on the
wire:

- A step's `input` is the array of its arguments.
- A step's `output`, and a callback's `output`, is a one-element array holding
  the result.

Object keys in `value` keep their order in the file. One case depends on that
order, so a harness must encode `value` without sorting its keys. Python's
`json` keeps the order. JavaScript's `JSON` keeps it except for integer-like
keys such as `"10"`, which it moves to the front, so no case depends on the
order of integer-like keys.

Errors aren't payloads. A step's error is a `StepError` object with `name` and
`message`. An attempt cut short by a crash counts toward the retry limit. The
SDK records it when it resumes the step, with this error:

```json
{
  "name": "AttemptInterrupted",
  "message": "the attempt was cut short by an infrastructure failure"
}
```

### History

`history.steps` holds one record per recorded step, in `seq` order:

```json
{
  "step_key": { "seq": 0 },
  "type": "inline",
  "task_name": "charge_card",
  "workflow_attempt": 0,
  "input": { "serializer": "json", "value": [100] },
  "output": { "serializer": "json", "value": ["ch_123"] },
  "started_at": "2026-10-14T12:00:00Z",
  "completed_at": "2026-10-14T12:00:01Z"
}
```

A step is finished exactly when `completed_at` is set, with either `output` or
`error`. An open step has neither.

`history.step_attempts` holds the failed attempts of open steps, in
`(seq, attempt)` order:

```json
{
  "step_key": { "seq": 1 },
  "attempt": 0,
  "workflow_attempt": 0,
  "error": { "name": "SmtpTimeout", "message": "smtp timed out" },
  "started_at": "2026-10-14T12:00:02Z",
  "ended_at": "2026-10-14T12:00:03Z"
}
```

Every `ctx` call has its own `seq`, starting at 0. The SDK leaves
`step_key.sub_key` unset: it's reserved for parallel steps, and GA needs only
`seq`.

### Exchanges

Each exchange is one request to a step route and its response:

```json
{
  "request": {
    "path": "/step-inline",
    "body": {
      "step_key": { "seq": 0 },
      "task_name": "charge_card",
      "kind": "start",
      "input": { "serializer": "json", "value": [100] },
      "started_at": "<any>"
    }
  },
  "response": { "status": 200, "body": { "applied": true } }
}
```

`/step-inline` is the only step route the cases use. A response body's payloads
use the same object form, and the harness encodes them before it answers.

### Callback

`callback` is the body of the `/callback` request that ends the attempt:

- A workflow that returns: `{ "complete": { "output": <payload> } }`. The
  workflow returns `{ "results": [...] }` (see [Programs](#programs)), so the
  output's `value` is a one-element array holding that object.
- A run that fails: `{ "error": { ... } }`. A determinism error sets `reason`
  and `determinism`. Any other failure has no `reason`.
- `null`: the attempt stops without sending a callback.

## Matching

A request or callback body matches its expected object when every key the case
lists matches.

- Keys the case doesn't list are ignored. A case doesn't list values the SDK
  chooses freely, such as an error's `stack` or a determinism error's
  human-readable `expected` and `actual`.
- `null` means the key must be absent (or `null`).
- `"<any>"` matches any value, as long as the key is present.
- A payload object matches a wire string whose base64 decodes to JSON equal to
  its `value`. Object key order doesn't matter here.
- Nested objects match by the same rules. Arrays must have the same length and
  match element by element.

## Programs

`workflow` is a list of calls. The workflow makes them in order, awaiting each
before the next, and returns `{ "results": [...] }`, with one result per call.
Each call names its `ctx` method in `method`. `run` is the only method so far.
Sleeps and detached tasks will add their own methods, with their own fields.

```json
{
  "method": "run",
  "name": "send_email",
  "args": ["ada@example.com"],
  "retry": { "max_retries": 3, "wait_duration_ms": 0 },
  "attempts": [
    { "raise": { "name": "SmtpTimeout", "message": "smtp timed out" } },
    { "return": "msg_456" }
  ],
  "catch": true
}
```

| Field | Meaning |
|---|---|
| `method` | The `ctx` method the call makes. `run` calls `ctx.run`. |
| `name` | The inline step's name. The harness runs a plain function with this name, or passes the name as the `name` option. |
| `args` | The arguments, passed positionally. Defaults to `[]`. |
| `retry` | The retry policy passed to `ctx.run`, if any. A case doesn't rely on the default when `retry` is absent: those steps succeed on their first attempt. |
| `attempts` | What the step function does each time this attempt calls it, in order: `{ "return": <value> }` or `{ "raise": { "name", "message" } }`. An empty list means the function must not run: its result comes from history, or the workflow never reaches the call. |
| `catch` | When true, the workflow catches an error from the call and carries on. A caught step error becomes that call's result, and nothing reports it, so the run can still succeed. A determinism error fails the run even when it's caught. |

`method` and `catch` apply to every call. The other fields belong to `run`.

A raised error's `name` is its type name: a harness raises an instance of an
exception class with that name (Python) or an `Error` whose `name` is set to it
(TypeScript). The SDK records that name and the message.

A call's result is the value `ctx.run` returned. When `catch` is true and the
call threw the SDK's step error, the result is
`{ "caught": { "name": <the original error's name>, "message": <its message> } }`.
A case only reads results from a workflow that returns, so what a harness
records for any other caught error doesn't matter.

## What the cases leave open

No case depends on these behaviors, so SDKs may differ on them:

- How many times an inline step retries when the call passes no `retry`.
- What a writer does after losing a failed-attempt write (`applied: false` on
  `kind: attempt`).
- How long the SDK keeps retrying a step write that gets 503, and whether it
  exits or waits after 409 `run_cancelled`. The cases only require a retry, and
  no callback after a cancel.
- What a step that returns nothing records as its output.
- Whether a run that fails because interrupted attempts used up a step's retries
  reports a `reason` on its failure callback. The cases that reach that point
  catch the error.
