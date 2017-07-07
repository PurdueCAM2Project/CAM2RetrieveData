import sys
import re
import argparse

class NameSpace(object):
    """A class used to create a namespace."""

    pass

def find_time(filename):
    m = re.search(r"(\d+)_(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{2})-"\
                  "\d{6}\.(png|jpg)", filename)
    if m:
        ns = NameSpace()
        ns.cam_id = m.group(1)
        ns.year = m.group(2)
        ns.month = m.group(3)
        ns.day = m.group(4)
        ns.hour = m.group(5)
        ns.minute = m.group(6)
        ns.sec = m.group(7)
        ns.ftype = m.group(8)
        return ns
        
    return None

def parse_args(args):
    parser = argparse.ArgumentParser(prog='getImgSets.py',\
                                     description='Gets a subset of images '\
                                     'from a file system based on a user '\
                                     'input file.', epilog='Note: Exactly '\
                                     'one of the -f and -c flags should be '\
                                     'asserted.')
    parser.add_argument('-r', '--read', help='asserting this flag will  '\
                        'read the input file with the name provided by the '\
                        'user, and then create the image subset.', type=str)
    parser.add_argument('-c', '--create', help='asserting this flag will '\
                        'create a template input file with the name provided '\
                        'by the user.', type=str)
    ns = parser.parse_args(args)
    if (ns.read is None and ns.create is None):
        parser.error("Exactly one of -r or -c must be asserted.")
    if (ns.read is not None and ns.create is not None):
        parser.error("Both -r and -c cannot be asserted.")
    return ns

def create_template(filename):
    f = open(filename, 'w')
    f.write('### Input file for getImgSets.py. For any numeric values, there '\
            'can be an upper\n### and lower bound. To express both an upper '\
            'and lower bound, use the form\n### \"lb,ub\". Use \",ub\" for '\
            'just an upper bund, \"lb,\" for just a lower bound, \n### or '\
            '\"num\" for an exact number. Otherwise, leave it blank.\n\n')
    f.write('# DIR is the directory from which to review image files\n')
    f.write('DIR=\n\n')
    f.write('YEAR=\n\n')
    f.write('MONTH=\n\n')
    f.write('DAY=\n\n')
    f.write('HOUR=\n\n')
    f.write('MIN=\n\n')
    f.write('SEC=\n')
    
def main(args):
    ns = parse_args(args)
    if (ns.read is not None):
        # A image subset will be created
        pass
    else:
        # A template file will be created
        create_template(ns.create)
    
if __name__ == "__main__":
    main(sys.argv[1:])
