import os
import sys
import shutil
import filecmp
import getFRNew
import time

if __name__ == '__main__':
    num_same = 0
    num_diff = 0
    i = 0
    j = 0
    while i < 10 and j < 20:
        print('i = {0:d}; j = {1:d}; same = {2:d}; diff = {3:d}'.\
              format(i, j, num_same, num_diff))
        args = ['', '-r', '100x100', '-t', '100', '-d', 'cam2', '0']
        getFRNew.main(args)
        if (os.path.isfile('results/105505/END.png')):
            i += 1
            if (filecmp.cmp('results/105505/REF.png',\
                            'results/105505/END.png')):
                num_same += 1
            else:
                num_diff += 1
        time.sleep(5)
        shutil.rmtree('results/105505')
        j += 1

    print("\nSame image {0:d} times\nDiff image {1:d} times".\
          format(num_same, num_diff))
