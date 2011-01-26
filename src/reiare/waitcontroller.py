#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-
"""
Access limit module
"""
import os
import fcntl
import pickle
import datetime
import time


class WaitController(object):
    """
    To use:

    >>> wc = WaitController('dummy.lock')
    >>> if wc.isLimiting():
    ...     wc.wating()

    execute something.

    >>> wc.release()

    >>> wc = WaitController('dummmy.lock', 2)
    >>> if os.path.isfile(wc.lock_file):
    ...     os.remove(wc.lock_file)
    >>> wc.isLimiting()
    True
    >>> time.sleep(2)
    >>> wc.isLimiting()
    False
    >>> wc.release()
    >>> wc._fp is None
    True
    """
    _lock_file = None
    _wait = None

    _fp = None

    def __init__(self, lock_file, wait=1, **opts):
        """
        >>> wc = WaitController()
        Traceback (most recent call last):
        ...
        TypeError: __init__() takes at least 2 arguments (1 given)
        >>> wc = WaitController('/tmp/waitcontroller.lock')
        >>> wc.lock_file
        '/tmp/waitcontroller.lock'
        >>> wc.wait
        1
        >>> wc = WaitController('dummy.lock', dummy='dummy')
        >>> wc.lock_file == os.path.join(os.getcwd(), 'dummy.lock')
        True
        >>> wc.dummy
        'dummy'
        >>> wc = WaitController('./dummy.lock')
        >>> wc.lock_file == os.path.join(os.getcwd(), './dummy.lock')
        True
        >>> wc = WaitController('dummy.lock', 'axbg')
        Traceback (most recent call last):
        ...
        ValueError: invalid literal for int() with base 10: 'axbg'
        """
        self.lock_file = lock_file
        if wait:
            self.wait = wait
        self.set_attrs(opts)

#     def __setattr__(self, attr, value):
#         """
#         >>> wc = WaitController('/tmp/waitcontroller.lock')
#         >>> wc.lock_file
#         '/tmp/waitcontroller.lock'
#         >>> wc.wait
#         1
#         >>> wc = WaitController('dummy.lock', dummy='dummy')
#         >>> wc.lock_file == os.path.join(os.getcwd(), 'dummy.lock')
#         True
#         >>> wc.dummy
#         'dummy'
#         >>> wc = WaitController('./dummy.lock')
#         >>> wc.lock_file == os.path.join(os.getcwd(), './dummy.lock')
#         True
#         >>> wc = WaitController('dummy.lock', 'axbg')
#         Traceback (most recent call last):
#         ...
#         ValueError: invalid literal for int() with base 10: 'axbg'
#         """
#         if attr == 'lock_file':
#             self.__dict__[attr] = os.path.join(os.getcwd(), value)
#         elif attr == 'wait':
#             self.__dict__[attr] = int(value)
#         else:
#             self.__dict__[attr] = value

    def set_attrs(self, dict):
        for k, v in dict.items():
            setattr(self, k, v)
#        [setattr(self, k, v) for k, v in dict.items()]

#     def __lock_file(self):
#         return self._lock_file

#     def ___lock_file(self):
#         return self.__lock_file()

    def __set_lock_file(self, value):
        """
        >>> wc = WaitController('dummy.lock')
        >>> wc.lock_file
        '/Users/tac/Dropbox/Project/Django/reiare/src/reiare/dummy.lock'
        >>> wc._WaitController__set_lock_file('test.lock')
        >>> wc.lock_file
        '/Users/tac/Dropbox/Project/Django/reiare/src/reiare/test.lock'
        """
        self._lock_file = os.path.join(os.getcwd(), value)

#     def ___set_lock_file(self, value):
#         self.__set_lock_file(value)

    #lock_file = property(___lock_file, ___set_lock_file, None, None)
    lock_file = property(lambda self: self._lock_file,
                         __set_lock_file, None, None)

#     def __wait(self):
#         return self._wait

#     def ___wait(self):
#         return self.__wait()

    def __set_wait(self, value):
        """
        >>> wc = WaitController('dummy.lock')
        >>> wc.wait
        1
        >>> wc._WaitController__set_wait(2)
        >>> wc.wait
        2
        >>> wc._WaitController__set_wait('aaa')
        Traceback (most recent call last):
        ...
        ValueError: invalid literal for int() with base 10: 'aaa'
        """
        self._wait = int(value)

#     def ___set_wait(self, value):
#         self.__set_wait(value)

    wait = property(lambda self: self._wait, __set_wait, None, None)

    def fp(self):
        """
        >>> wc = WaitController('dummy.lock')
        >>> wc.lock_file == os.path.join(os.getcwd(), 'dummy.lock')
        True
        >>> wc.fp().__class__
        <type 'file'>
        """
        if self._fp == None:
            self.lock()
        return self._fp

    def _read_lock(self):
        """
        >>> wc = WaitController('dummy.lock')
        >>> wc._read_lock()
        >>> wc._fp.mode
        'r+'
        >>> wc.release()
        """
        self._fp = file(self.lock_file, 'r+')
        fcntl.flock(self._fp.fileno(), fcntl.LOCK_EX)

    def _write_lock(self):
        """
        >>> wc = WaitController('dummy.lock')
        >>> wc._write_lock()
        >>> wc._fp.mode
        'w+'
        >>> wc.release()
        """
        self._fp = file(self.lock_file, 'w+')
        fcntl.flock(self._fp.fileno(), fcntl.LOCK_EX)

    def lock(self):
        """
        >>> wc = WaitController('dummy.lock')
        >>> wc.lock()
        >>> wc._fp.__class__
        <type 'file'>
        >>> wc.release()
        """
        if not os.path.isfile(self.lock_file):
            self._write_lock()
            pickle.dump(datetime.datetime.now()
                        - datetime.timedelta(seconds=self.wait), self._fp)
            self._fp.seek(0)
        else:
            self._read_lock()

    def unlock(self):
        """
        >>> wc = WaitController('dummy.lock')
        >>> wc.lock()
        >>> wc.unlock()
        >>> wc._fp is None
        True
        """
        fcntl.flock(self._fp.fileno(), fcntl.LOCK_UN)
        self._fp.close()
        self._fp = None

    def latest_datetime(self):
        self.fp().seek(0)
        return pickle.load(self.fp())

    def update_latest_datetime(self):
        self.fp().seek(0)
        pickle.dump(datetime.datetime.now(), self.fp())
        self.fp().truncate()

    def isLimiting(self):
        """
        >>> wc = WaitController('dummy.lock')
        >>> time.sleep(1)
        >>> wc.isLimiting()
        False
        >>> wc.release()
        """
        return (datetime.datetime.now() - self.latest_datetime()) \
            < datetime.timedelta(seconds=self.wait)

    def waiting(self):
        time.sleep(self.wait)

    def release(self):
        self.update_latest_datetime()
        self.unlock()

# class WaitController2(WaitController):
#     """
#     >>> wc = WaitController2('dummy.lock')
#     >>> wc.lock_file
#     >>> wc.lock_file = 'dummy.lock'
#     >>> wc.lock_file
#     >>> wc._WaitController2__set_lock_file('dummy.lock')
#     >>> wc.lock_file
#     """
#     def __set_lock_file(self, value):
#         print '__set_lock_file'
#         self._lock_file = value

#     def ___set_lock_file(self, value):
#         print '___set_lock_file'
#         #self._lock_file = value
#         self.__set_lock_file(value)

#     #lock_file = property(lambda self: self._lock_file,
#        ___set_lock_file, None, None)


def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()

