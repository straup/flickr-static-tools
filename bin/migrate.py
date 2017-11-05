#!/usr/bin/env python

import os
import sys
import logging
import shutil

if __name__ == "__main__":

    source = sys.argv[1]
    dest = sys.argv[2]

    for path in sys.argv[3:]:

        old_root = os.path.join(source, path)
        new_root = os.path.join(dest, path)

        if not os.path.exists(old_root):
            logging.error("%s does not exist" % old_root)
            sys.exit(1)

        if not os.path.exists(new_root):
            os.makedirs(new_root)

        for (root, dirs, files) in os.walk(old_root):

            for fname in files:    
                
                old_file = os.path.join(old_root, fname)
                new_file = os.path.join(new_root, fname)
        
                print "move %s to %s" % (old_file, new_file)
                shutil.copy(old_file, new_file)
              
        shutil.rmtree(old_root)
