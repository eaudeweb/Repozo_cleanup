#!/usr/bin/env python
import os
import sys
import getopt

commit = False
rec = False

def valid_exts(file):
    return file.endswith('.dat') or\
            file.endswith('.fsz') or\
            file.endswith('.deltafsz')

def filter_files(p, filenames):
    filenames.sort()
    filenames = [os.path.join(p, f) for f in filenames]
    valid_files = filter(valid_exts, filenames)
    invalid_files = filter(lambda s: s not in valid_files, filenames)

    for file in invalid_files:
        print "Ignoring file", file

    if len(valid_files) == 0:
        print "Directory", p, "contains no repozos files"
        return

    index = -1
    for i in range(len(valid_files)-1, -1, -1):
        if valid_files[i].endswith('.dat'):
            index = i
            break
    else:
        print "No pack in directory", p
        return

    if index == 0:
        print "Directory", p, "clean"
        return

    to_delete = valid_files[0:index]
    for f in to_delete:
        if not commit:
            print "Will delete", f
        else:
            os.remove(f)

def walk_dir(dir):
    for (dirpath, dirname, filenames) in os.walk(dir):
        if not rec:
            del dirname[0:len(dirname)] # don't recurse
        filter_files(dirpath, filenames)

def usage():
    print 'Usage:'
    print '     ./clean_repozos [opts] PATH'
    print
    print 'Removes packed files from repozos directories'
    print
    print 'Options:'
    print '     -r = do a recursive search'
    print '     -c = commit the changes (don\'t do a dry run - default. delete files instead'
    print '     -h = print this message'

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "rch")
    except getopt.GetoptError, e:
        print str(e)
        usage()
        sys.exit(-1)

    opts = [t[0] for t in opts]
    if '-h' in opts or len(args) == 0:
        usage()
        sys.exit(0)
    if '-r' in opts:
        rec = True
    if '-c' in opts:
        commit = True

    walk_dir(args[0])

