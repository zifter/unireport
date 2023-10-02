def as_bool(value: str) -> bool:
    """
    Given a string value that represents True or False, returns the Boolean equivalent.
    Heavily inspired from distutils strtobool.

    From `isort`: https://github.com/PyCQA/isort/blob/5.10.1/isort/settings.py#L915-L922
    """

    if value is None:
        return False

    if isinstance(value, bool):
        return value

    _STR_BOOLEAN_MAPPING = {
        "y": True,
        "yes": True,
        "t": True,
        "on": True,
        "1": True,
        "true": True,
        "n": False,
        "no": False,
        "f": False,
        "off": False,
        "0": False,
        "false": False,
    }
    return _STR_BOOLEAN_MAPPING[value.lower()]
