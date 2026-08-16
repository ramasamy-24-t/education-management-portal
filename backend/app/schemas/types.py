from typing import Annotated

from pydantic import AfterValidator


def _normalize_email(value: str) -> str:
    email = value.strip().lower()
    local, _, domain = email.partition("@")
    if not local or not domain or "." not in domain:
        raise ValueError("Invalid email address")
    return email


EmailAddress = Annotated[str, AfterValidator(_normalize_email)]
