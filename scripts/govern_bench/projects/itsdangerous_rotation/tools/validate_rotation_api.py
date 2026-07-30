"""Public smoke validator for the T30 key-rotation API."""

from __future__ import annotations

from itsdangerous import Serializer
from itsdangerous import TimedSerializer


def main() -> int:
    current = Serializer(["old-secret", "new-secret"])
    old = Serializer("old-secret").dumps({"scope": "public"})
    new = current.dumps({"scope": "public"})

    new_payload, new_reissue = current.loads_with_reissue(new)
    old_payload, old_reissue = current.loads_with_reissue(old)
    assert new_payload == old_payload == {"scope": "public"}
    assert new_reissue is False
    assert old_reissue is True

    timed = TimedSerializer(["old-secret", "new-secret"])
    timed_payload, timed_reissue = timed.loads_with_reissue(timed.dumps("ok"))
    assert timed_payload == "ok"
    assert timed_reissue is False
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
