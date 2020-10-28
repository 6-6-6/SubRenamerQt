#!/usr/bin/python
# -*- coding:utf-8 -*-

import mimetypes
from pathlib import Path

subtitleExtensions = (
    ".ass",
    ".sbv",
    ".ssa",
    ".srt")


def toOrdinal(num):
    assert(num > 0)
    flag = num // 10 % 10 != 1
    numMod = num % 10
    if numMod == 1 and flag:
        return f"{num}st"
    elif numMod == 2 and flag:
        return f"{num}nd"
    elif numMod == 3 and flag:
        return f"{num}rd"
    else:
        return f"{num}th"


def removeNonTargetFiles(fileList, hint='video'):
    ret = []
    # switch, filter different type of files, depending on hint provided
    if hint == 'video':
        for f in fileList:
            if str(mimetypes.guess_type(f)[0]).startswith('video'):
                ret.append(f)
    elif hint == 'subtitle':
        for f in fileList:
            if str(f).lower().endswith(subtitleExtensions):
                ret.append(f)
    #
    return ret
