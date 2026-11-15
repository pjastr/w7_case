"""Several actions of one rule – report ALL differences, not only the first one."""


def check_actions(actual: dict, expected: dict) -> None:
    """Compares dicts of actions and reports every difference at once.

    A plain sequence of asserts stops at the first mismatch; here the
    message lists all of them (slide "Wiele akcji – zbieranie niezgodności").
    """
    different = [f"{name}: is {actual.get(name)!r}, "
                 f"expected {value!r}"
                 for name, value in expected.items()
                 if actual.get(name) != value]
    assert not different, "\n".join(different)
