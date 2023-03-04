from __future__ import absolute_import, division, print_function

import io  # noqa: F401

from reportyy import six


def utf8(value):
    if six.PY2 and isinstance(value, six.text_type):
        return value.encode("utf-8")
    else:
        return value
