"""Public smoke validator for the T30 key-rotation API."""

from __future__ import annotations

from datetime import datetime

from itsdangerous import Serializer
from itsdangerous import SignatureExpired
from itsdangerous import TimedSerializer
from itsdangerous import URLSafeSerializer
from itsdangerous import URLSafeTimedSerializer


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
    timed_current = timed.dumps("ok")
    timed_old = TimedSerializer("old-secret").dumps("old")
    timed_payload, timed_reissue = timed.loads_with_reissue(timed_current)
    assert timed_payload == "ok"
    assert timed_reissue is False

    old_payload, old_reissue = timed.loads_with_reissue(timed_old)
    assert old_payload == "old"
    assert old_reissue is True

    timestamp_payload, timestamp, timestamp_reissue = timed.loads_with_reissue(
        timed_old,
        return_timestamp=True,
    )
    assert timestamp_payload == "old"
    assert isinstance(timestamp, datetime)
    assert timestamp_reissue is True

    try:
        timed.loads_with_reissue(timed_old, max_age=-1)
    except SignatureExpired:
        pass
    else:
        raise AssertionError(
            "expired timed values must retain SignatureExpired behavior"
        )

    url_safe = URLSafeSerializer(["old-secret", "new-secret"])
    assert url_safe.loads_with_reissue(url_safe.dumps({"url": "safe"})) == (
        {"url": "safe"},
        False,
    )
    url_safe_timed = URLSafeTimedSerializer(["old-secret", "new-secret"])
    assert url_safe_timed.loads_with_reissue(
        url_safe_timed.dumps({"url": "timed"})
    ) == (
        {"url": "timed"},
        False,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
