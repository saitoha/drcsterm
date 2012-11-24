#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ***** BEGIN LICENSE BLOCK *****
# Copyright (C) 2012  Hayaki Saito <user@zuse.jp>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ***** END LICENSE BLOCK *****

def main():
    import sys, os, optparse, select

    # parse options and arguments
    usage = 'usage: %prog [options] [command | - ]'
    parser = optparse.OptionParser(usage=usage)

    parser.add_option('--version', dest='version',
                      action="store_true", default=False,
                      help='show version')

    parser.add_option('-t', '--term', dest='term',
                      help='override TERM environment variable')

    parser.add_option('-o', '--outenc', dest='enc',
                      help='set output encoding')

    (options, args) = parser.parse_args()

    if options.version:
        import __init__
        print '''
drcsterm %s 
Copyright (C) 2012 Hayaki Saito <user@zuse.jp>. 

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see http://www.gnu.org/licenses/.
        ''' % __init__.__version__
        return

    # retrive terminal encoding setting
    import locale
    language, encoding = locale.getdefaultlocale()
    termenc = encoding
    assert termenc.lower() == "utf-8"
    lang = '%s.%s' % (language, "UTF-8") 

    # retrive starting command
    if len(args) > 0:
        command = args[0]
    elif not os.getenv('SHELL') is None:
        command = os.getenv('SHELL')
    else:
        command = '/bin/sh'

    # retrive TERM setting
    if options.term:
        term = options.term
    elif not os.getenv('TERM') is None:
        term = os.getenv('TERM')
    else:
        term = 'xterm'

    import tff
    
    ################################################################################
    #
    # Scanner implementation
    #
    class UnicodeDRCSScanner(tff.Scanner):
        ''' scan input stream and iterate characters '''
        __data = None
    
        def assign(self, value, termenc):
            self.__data = value
    
        def __iter__(self):
            for x in self.__data:
                c = ord(x)
                if c < 0x80:
                    # 0xxxxxxx
                    self.__utf8_state = 0
                    self.__count = 0
                    yield c
                elif c >> 6 == 0x02:
                    # 10xxxxxx
                    self.__utf8_state = self.__utf8_state << 6 | c & 0x3f
                    self.__count -= 1
                    if self.__count == 0:
                        # TODO: convert all redundant utf-8 sequences into '?'
                        if self.__utf8_state < 0x80:
                            yield 0x3f
                        else:
                            code = self.__utf8_state
                            if code >= 0x100000:
                                yield 0x1b # ESC
                                yield 0x28 # (
                                yield 0x20 # SP
                                yield (code >> 8) & 0xff # (
                                yield code & 0xff
                                yield 0x1b # ESC
                                yield 0x28 # (
                                yield 0x42 # B
                            else:
                                yield code 
                        self.__count = 0
                        self.__utf8_state = 0
    
                elif c >> 5 == 0x06:
                    # 110xxxxx 10xxxxxx
                    if self.__count != 0:
                        self.__count = 0
                        yield 0x3f
                    else:
                        self.__utf8_state = c & 0x1f
                        self.__count = 1
                elif c >> 4 == 0x0e:
                    # 1110xxxx 10xxxxxx 10xxxxxx
                    if self.__count != 0:
                        self.__count = 0
                        yield 0x3f
                    else:
                        self.__utf8_state = c & 0x0f
                        self.__count = 2
                elif c >> 3 == 0x1e:
                    # 11110xxx
                    if self.__count != 0:
                        self.__count = 0
                        yield 0x3f
                    else:
                        self.__utf8_state = c & 0x07
                        self.__count = 3
                elif c >> 2 == 0x3e:
                    # 111110xx
                    if self.__count != 0:
                        self.__count = 0
                        yield 0x3f
                    else:
                        self.__utf8_state = c & 0x03
                        self.__count = 4
                elif c >> 1 == 0x7e:
                    # 1111110x
                    if self.__count != 0:
                        self.__count = 0
                        yield 0x3f
                    else:
                        self.__utf8_state = c & 0x01
                        self.__count = 5

    tty = tff.DefaultPTY(term, lang, command, sys.stdin)
    tty.fitsize()
    session = tff.Session(tty)
    session.start("UTF-8", outputscanner=UnicodeDRCSScanner())


''' main '''
if __name__ == '__main__':    
    main()

