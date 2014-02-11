DRCSTerm
========

What is This
------------

  DRCSTerm aims at reviving the DRCS(Dynamically Redefined Character Set)
  feature to the Terminal World.
  It provides the character mapping service which converts some UCS Private
  Area (Plain 16) characters to ISO-2022 designation sequences on your terminal.
  

Enable/Disable Mapping
----------------------

DRCSTerm reserves private mode 8800-8804.

Private mode 8800(DRCSMMv1) enables or disables the character mapping service.

Example for DRCSMMv1:

- Enable mapping service version 1::

    CSI ? 8800 h

- Disable mapping service version 1::

    CSI ? 8800 l

Mapping Rule Version 1
----------------------

  DRCSTerm uses UCS 16 Plane (U+100000-U+10FFFF).
  If output character stream includes characters in this range, such as; ::

     U+10XXYY ( 0x40 <= 0xXX <=0x7E, 0x20 <= 0xYY <= 0x7F )

  DRCSTerm convert them into fllowing ISO-2022 Designatin Format:

  ESC ( SP <\\xXX> <\\xYY> ESC ( B


Install
-------

via github ::

    $ git clone --recursive https://github.com/saitoha/drcsterm.git
    $ cd drcsterm
    $ python setup.py install

or via pip ::

    $ pip install drcsterm


Usage
-----

::

    $ drcsterm [options] command


* Options::

    -h, --help                  show this help message and exit
    --version                   show version
    -t TERM, --term=TERM        override TERM environment variable

Dependency
----------

 - Hayaki Saito's TFF, Terminal Filter Framework
   https://github.com/saitoha/tff

Reference
---------

 - "VT320 Soft Character Sets" http://vt100.net/dec/vt320/soft_characters
 - "VT100.net - DECDLD" http://vt100.net/docs/vt510-rm/DECDLD
 - "RLogin" http://nanno.dip.jp/softlib/man/rlogin/
   This terminal supports DECDLD
 - "Soft Character Set (DRCS)" (Japanese) http://togetter.com/li/385813

