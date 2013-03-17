import sys

_ver = sys.version_info

#: Python 2.x?
is_py2 = (_ver[0] == 2)

#: Python 3.x?
is_py3 = (_ver[0] == 3)


if is_py2:
    def update_doc(method, newdoc):
        method.im_func.func_doc = newdoc

    basestring = basestring
elif is_py3:
    def update_doc(method, newdoc):
        method.__doc__ = newdoc

    basestring = (str, bytes)
