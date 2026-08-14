"""A tiny app for the QA agent to answer questions about."""

GREETING = "hello dojo"


def greet(name: str) -> str:
    """Return the standard greeting for a name."""
    return f"{GREETING}, {name}"


if __name__ == "__main__":
    print(greet("agent"))
