#!/usr/bin/env python3
"""Check that every workflow golden fixture follows the format in README.md.

Standard library only: CI runs it with a bare python3.
"""

import json
import sys
from pathlib import Path
from typing import Any

CASES = Path(__file__).parent / "cases"

CASE_KEYS = {"description", "attempt", "history", "workflow", "exchanges", "callback"}
# The keys a call may set, by its ctx method. Sleeps and detached tasks will add
# their own methods.
CALL_KEYS = {"run": {"method", "name", "args", "retry", "attempts", "catch"}}
STEP_TYPES = {"inline", "detached", "sleep"}
STEP_ROUTES = {"/step-inline"}
KINDS = {"start", "attempt", "complete"}
# The matcher ignores keys a case leaves out, so a missing one would silently
# weaken the case instead of failing it.
REQUIRED_BY_KIND = {
    "start": ("input", "started_at"),
    "attempt": ("attempt", "error", "started_at"),
    "complete": (),
}


def seq_of(value: dict[str, Any], default: Any = None) -> Any:
    key = value.get("step_key")
    return key.get("seq", default) if isinstance(key, dict) else default


class Checker:
    def __init__(self, name: str) -> None:
        self.name = name
        self.problems: list[str] = []

    def fail(self, where: str, message: str) -> None:
        self.problems.append(f"{self.name}: {where}: {message}")

    def payload(self, where: str, value: Any) -> None:
        if not isinstance(value, dict) or set(value) != {"serializer", "value"}:
            self.fail(where, 'a payload must be {"serializer": ..., "value": ...}')
        elif value["serializer"] != "json":
            self.fail(where, f"unknown serializer {value['serializer']!r}")

    def error(self, where: str, value: Any) -> None:
        if not isinstance(value, dict) or not {"name", "message"} <= set(value):
            self.fail(where, "an error needs a name and a message")

    def key(self, where: str, value: dict[str, Any]) -> None:
        if "idx" in value or "seq" in value:
            self.fail(
                where, "steps are keyed by step_key alone; a case has no idx or seq"
            )
        key = value.get("step_key")
        if not isinstance(key, dict):
            self.fail(where, 'step_key must be {"seq": ...}')
        elif not isinstance(key.get("seq"), int) or key["seq"] < 0:
            self.fail(f"{where}.step_key", "seq must be a non-negative integer")
        elif set(key) != {"seq"}:
            self.fail(f"{where}.step_key", "the SDK leaves sub_key unset at GA")

    def step(self, where: str, step: Any) -> None:
        if not isinstance(step, dict):
            self.fail(where, "a step record must be an object")
            return
        self.key(where, step)
        for field in ("type", "workflow_attempt", "input", "started_at"):
            if field not in step:
                self.fail(where, f"missing {field}")
        if (
            step.get("type") in STEP_TYPES
            and step["type"] != "sleep"
            and not step.get("task_name")
        ):
            self.fail(where, "missing task_name")
        self.payload(f"{where}.input", step.get("input"))
        if "output" in step:
            self.payload(f"{where}.output", step["output"])
        if "error" in step:
            self.error(f"{where}.error", step["error"])
        if "output" in step and "error" in step:
            self.fail(where, "a step has an output or an error, not both")
        finished = "output" in step or "error" in step
        if finished != ("completed_at" in step):
            self.fail(where, "completed_at is set exactly when the step has an outcome")

    def step_attempt(self, where: str, attempt: Any) -> None:
        if not isinstance(attempt, dict):
            self.fail(where, "a step attempt must be an object")
            return
        self.key(where, attempt)
        for field in ("attempt", "workflow_attempt", "error", "ended_at"):
            if field not in attempt:
                self.fail(where, f"missing {field}")
        if "failed_at" in attempt:
            self.fail(where, "a failed attempt's end time is ended_at")
        self.error(f"{where}.error", attempt.get("error"))

    def history(self, history: Any) -> None:
        if not isinstance(history, dict) or set(history) != {"steps", "step_attempts"}:
            self.fail("history", "must have exactly steps and step_attempts")
            return
        if not all(isinstance(history[k], list) for k in ("steps", "step_attempts")):
            self.fail("history", "steps and step_attempts must be lists")
            return
        for i, step in enumerate(history["steps"]):
            self.step(f"history.steps[{i}]", step)
        for i, attempt in enumerate(history["step_attempts"]):
            self.step_attempt(f"history.step_attempts[{i}]", attempt)
        steps = [s for s in history["steps"] if isinstance(s, dict)]
        seqs = [seq_of(s) for s in steps]
        if seqs != sorted(set(seqs), key=lambda s: (s is None, s)):
            self.fail("history.steps", "steps must be in seq order, one per seq")
        attempts = [a for a in history["step_attempts"] if isinstance(a, dict)]
        keys = [(seq_of(a, -1), a.get("attempt", -1)) for a in attempts]
        if keys != sorted(set(keys)):
            self.fail(
                "history.step_attempts",
                "must be in (seq, attempt) order, one per attempt",
            )
        open_seqs = {seq_of(s) for s in steps if "completed_at" not in s}
        for i, attempt in enumerate(attempts):
            if seq_of(attempt) not in open_seqs:
                self.fail(
                    f"history.step_attempts[{i}]",
                    "a failed attempt belongs to an open step",
                )

    def call(self, where: str, call: Any) -> None:
        if not isinstance(call, dict) or call.get("method") not in CALL_KEYS:
            self.fail(where, f"a call needs a method, one of {sorted(CALL_KEYS)}")
            return
        unknown = set(call) - CALL_KEYS[call["method"]]
        if unknown:
            self.fail(where, f"unknown keys {sorted(unknown)}")
        if not isinstance(call.get("catch", False), bool):
            self.fail(where, "catch must be true or false")
        if call["method"] == "run":
            self.run(where, call)

    def run(self, where: str, call: dict[str, Any]) -> None:
        if not isinstance(call.get("name"), str) or not call["name"]:
            self.fail(where, "a run call needs a step name in name")
        if not isinstance(call.get("args", []), list):
            self.fail(where, "args must be a list")
        retry = call.get("retry")
        max_retries = retry.get("max_retries") if isinstance(retry, dict) else None
        if retry is not None and (
            not isinstance(max_retries, int)
            or max_retries < 0
            or retry.get("wait_duration_ms") != 0
        ):
            self.fail(
                f"{where}.retry",
                "needs max_retries of at least 0 and wait_duration_ms: 0",
            )
            max_retries = None
        attempts = call.get("attempts")
        if not isinstance(attempts, list):
            self.fail(where, "attempts must be a list")
            return
        for i, attempt in enumerate(attempts):
            if not isinstance(attempt, dict) or len(attempt) != 1:
                self.fail(f"{where}.attempts[{i}]", "must be one of return or raise")
            elif "raise" in attempt:
                self.error(f"{where}.attempts[{i}].raise", attempt["raise"])
            elif "return" not in attempt:
                self.fail(f"{where}.attempts[{i}]", "must be one of return or raise")
        raises = any(isinstance(a, dict) and "raise" in a for a in attempts)
        if retry is None and raises:
            self.fail(where, "a call that raises sets retry: the default count is open")
        if max_retries is not None and len(attempts) > max_retries + 1:
            self.fail(where, "more attempts than the retry policy allows")

    def exchange(self, where: str, exchange: Any) -> None:
        if not isinstance(exchange, dict) or set(exchange) != {"request", "response"}:
            self.fail(where, "must have exactly request and response")
            return
        request, response = exchange["request"], exchange["response"]
        if request.get("path") not in STEP_ROUTES:
            self.fail(f"{where}.request", f"path must be one of {sorted(STEP_ROUTES)}")
        body = request.get("body")
        if not isinstance(body, dict):
            self.fail(f"{where}.request", "missing body")
            return
        self.key(f"{where}.request.body", body)
        kind = body.get("kind")
        if kind not in KINDS:
            self.fail(f"{where}.request.body", f"kind must be one of {sorted(KINDS)}")
        for field in REQUIRED_BY_KIND.get(kind, ()):
            if body.get(field) is None:
                self.fail(f"{where}.request.body", f"kind {kind} needs {field}")
        attempt = body.get("attempt")
        if (
            kind == "attempt"
            and attempt is not None
            and (
                not isinstance(attempt, int) or isinstance(attempt, bool) or attempt < 0
            )
        ):
            self.fail(f"{where}.request.body", "attempt must be a non-negative integer")
        if kind == "complete" and (body.get("output") is None) == (
            body.get("error") is None
        ):
            self.fail(f"{where}.request.body", "a complete needs output or error")
        for field in ("input", "output"):
            if body.get(field) is not None:
                self.payload(f"{where}.request.body.{field}", body[field])
        if body.get("error") is not None:
            self.error(f"{where}.request.body.error", body["error"])
        if not isinstance(response, dict) or not isinstance(
            response.get("status"), int
        ):
            self.fail(f"{where}.response", "needs a status")
            return
        if response["status"] == 200:
            rbody = response.get("body")
            if not isinstance(rbody, dict) or not isinstance(
                rbody.get("applied"), bool
            ):
                self.fail(f"{where}.response.body", "a 200 needs applied")
            elif not rbody["applied"] and kind != "attempt" and "step" not in rbody:
                self.fail(f"{where}.response.body", f"a lost {kind} returns the row")
            elif "step" in rbody:
                self.step(f"{where}.response.body.step", rbody["step"])
                if seq_of(rbody["step"]) != seq_of(body):
                    self.fail(
                        f"{where}.response.body.step",
                        "the returned row is for another seq",
                    )

    def callback(self, callback: Any) -> None:
        if callback is None:
            return
        outcome = {k: v for k, v in callback.items() if v is not None}
        if set(outcome) == {"complete"}:
            self.payload("callback.complete.output", outcome["complete"].get("output"))
        elif set(outcome) == {"error"}:
            details = outcome["error"].get("determinism")
            if (details is not None) != (
                outcome["error"].get("reason") == "DeterminismError"
            ):
                self.fail(
                    "callback.error",
                    "determinism is set exactly when reason is DeterminismError",
                )
            if details is None and "reason" not in outcome["error"]:
                self.fail("callback.error", "list reason: null for a plain failure")
            if details is not None:
                self.key("callback.error.determinism", details)
                if details.get("kind") not in {"input_hash", "type", "unknown_type"}:
                    self.fail("callback.error.determinism", "unknown kind")
        else:
            self.fail(
                "callback", "must set exactly one of complete or error, or be null"
            )

    def case(self, case: Any) -> None:
        if not isinstance(case, dict):
            self.fail("case", "must be an object")
            return
        missing = CASE_KEYS - {"history"} - set(case)
        if missing:
            self.fail("case", f"missing {sorted(missing)}")
        if set(case) - CASE_KEYS:
            self.fail("case", f"unknown keys {sorted(set(case) - CASE_KEYS)}")
        attempt = case.get("attempt")
        if not isinstance(attempt, int) or attempt < 0:
            self.fail("attempt", "must be a non-negative integer")
        elif (attempt == 0) == ("history" in case):
            self.fail("history", "is absent exactly when attempt is 0")
        if "history" in case:
            self.history(case["history"])
        for i, call in enumerate(case.get("workflow") or []):
            self.call(f"workflow[{i}]", call)
        for i, exchange in enumerate(case.get("exchanges") or []):
            self.exchange(f"exchanges[{i}]", exchange)
        self.callback(case.get("callback"))


# Stricter than json.loads, which accepts NaN and duplicate keys that JavaScript
# rejects or resolves differently.
def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    keys = [key for key, _ in pairs]
    duplicates = sorted({key for key in keys if keys.count(key) > 1})
    if duplicates:
        raise ValueError(f"duplicate keys {duplicates}")
    return dict(pairs)


def reject_constant(name: str) -> Any:
    raise ValueError(f"{name} isn't JSON")


def main() -> int:
    paths = sorted(CASES.glob("*.json"))
    if not paths:
        print(f"no cases in {CASES}", file=sys.stderr)
        return 1
    problems: list[str] = []
    for path in paths:
        checker = Checker(path.name)
        try:
            case = json.loads(
                path.read_text(),
                object_pairs_hook=strict_object,
                parse_constant=reject_constant,
            )
        except ValueError as e:
            checker.fail("file", f"invalid JSON: {e}")
        else:
            try:
                checker.case(case)
            except (AttributeError, KeyError, TypeError) as e:
                checker.fail("file", f"malformed case ({type(e).__name__}: {e})")
        problems += checker.problems
    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        return 1
    print(f"{len(paths)} cases OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
