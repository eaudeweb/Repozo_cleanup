#!/usr/bin/env python
import unittest
import os
import sys
from subprocess import Popen, PIPE, call

class CleanRepozoTestCase(unittest.TestCase):
    def test_noargs(self):
        """
        Tests for printing usage msg if no args are given
        """
        result = Popen(['./clean_repozos.py'], stdout=PIPE).communicate()[0]
        self.assertEquals(result.split('\n')[0], 'Usage:', 'No help printed')
        self.assertEquals(len(result.split('\n')), 10)
    
    def test_onlyhelp(self):
        """
        Tests for printing usage msg if only -h is given
        """
        result = Popen(['./clean_repozos.py', '-h'], stdout=PIPE).communicate()[0]
        self.assertEquals(result.split('\n')[0], 'Usage:', 'No help printed')
        self.assertEquals(len(result.split('\n')), 10, 'Invalid message printed')
    
    def test_help(self):
        """
        Tests for printing usage msg if -h is given
        """
        result = Popen(['./clean_repozos.py', '-rh'], stdout=PIPE).communicate()[0]
        self.assertEquals(result.split('\n')[0], 'Usage:', 'No help printed')
        self.assertEquals(len(result.split('\n')), 10, 'Invalid message printed')

    def test_nofiles(self):
        """
        Tests for directories with no repozos files
        """
        result = Popen(['./clean_repozos.py', '1_data'], stdout=PIPE).communicate()[0]
        self.assertEquals(result.split('\n')[0], 'Directory 1_data contains no repozos files')
        self.assertEquals(len(result.split('\n')), 2, 'Invalid message printed')

    def test_rec(self):
        """
        Tests for recursive option handling.
        """
        result = Popen(['./clean_repozos.py', '-r', '1_data'], stdout=PIPE).communicate()[0]
        self.assertEquals(result.split('\n')[0], 'Directory 1_data contains no repozos files')
        self.assertEquals(len(result.split('\n')), 12, 'Invalid message printed')

    def test_delete(self):
        """
        Tests for deletion (only dry run) of files.
        """
        result = Popen(['./clean_repozos.py', '1_data/1'], stdout=PIPE).communicate()[0]
        for f in result.split('\n')[1:]:
            if f:
                self.assertTrue(f.startswith('Will delete '), 'Will not delete deleteable file')
        self.assertEquals(len(result.split('\n')), 11)#, 'Invalid message printed')

    def test_clean(self):
        """
        Tests for clean directory.
        """
        result = Popen(['./clean_repozos.py', '2_data/2'], stdout=PIPE).communicate()[0]
        self.assertEquals(result.split('\n')[0], 'Directory 2_data/2 clean', 'Clean directory reported as dirty')
        self.assertEquals(len(result.split('\n')), 2, 'Invalid message printed')

    def test_ignoring(self):
        """
        Tests for ignoring invalid files.
        """
        result = Popen(['./clean_repozos.py', '1_data/1'], stdout=PIPE).communicate()[0]
        self.assertTrue(result.split('\n')[0].startswith('Ignoring file '), 'First file should be ignored')
        self.assertEquals(len(result.split('\n')), 11, 'Invalid message printed')

    def test_commit(self):
        """
        Tests for actual deletion of files. Does a full run first, deleting
        files from a copy and checks whether the subsequent dry run outputs
        one more line, claiming that the directory is clean.
        """
        call(['mkdir', '-p', '/tmp'])
        call(['cp', '-r', '1_data/', 'tmp'])

        result = Popen(['./clean_repozos.py', '-rc', 'tmp/'], stdout=PIPE).communicate()[0]
        l = len(result.split('\n'))

        result = Popen(['./clean_repozos.py', '-r', 'tmp/'], stdout=PIPE).communicate()[0]
        self.assertEquals(len(result.split('\n')), 1 + l, 
                "The directory was not cleaned or more files were added to it during the test")

        ok = False
        for line in result.split('\n'):
            if line.endswith('clean'):
                ok = True
                break
        self.assertTrue(ok, "No line saying that the directory is clean")

    def tearDown(self):
        call(['rm', '-rf', 'tmp'])


def test_suite():
    return unittest.TestSuite([
        unittest.makeSuite(CleanRepozoTestCase)])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
