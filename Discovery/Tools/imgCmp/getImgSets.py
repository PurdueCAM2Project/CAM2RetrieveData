import sys
import os
import re
import argparse
import shutil

class NameSpace(object):
    """A class used to create a namespace."""

    pass

def get_img_info(filename):
    m = re.search(r"(\d+)_(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{2})-"\
                  "\d{6}\.(png|jpg)", filename)
    if m:
        ns = NameSpace()
        ns.camid = int(m.group(1))
        ns.year = int(m.group(2))
        ns.month = int(m.group(3))
        ns.day = int(m.group(4))
        ns.hour = int(m.group(5))
        ns.mnt = int(m.group(6)) # min is a keyword
        ns.sec = int(m.group(7))
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

def create_template(outputfile):
    f = open(outputfile, 'w')
    f.write('### Input file for getImgSets.py. For any numeric values, there '\
            'can be an upper\n### and lower bound. To express both an upper '\
            'and lower bound, use the form\n### \"lb,ub\". Use \",ub\" for '\
            'just an upper bund, \"lb,\" for just a lower bound, \n### or '\
            '\"num\" for an exact number. Otherwise, leave it blank.\n\n')
    f.write('# READDIR is the directory from which to review image files\n')
    f.write('READDIR=\n\n')
    f.write('# WRITEDIR is the directory in which to save image files\n')
    f.write('WRITEDIR=\n\n')
    f.write('# ID refers to the camera id in the database\n')
    f.write('ID_RANGE=\nID_INTERVAL=\n\n')
    f.write('YEAR_RANGE=\nYEAR_INTERVAL=\n\n')
    f.write('MONTH_RANGE=\nMONTH_INTERVAL=\n\n')
    f.write('DAY_RANGE=\nDAY_INTERVAL=\n\n')
    f.write('HOUR_RANGE=\nHOUR_INTERVAL=\n\n')
    f.write('MINUTE_RANGE=\nMINUTE_INTERVAL=\n\n')
    f.write('SECOND_RANGE=\nSECOND_INTERVAL=\n')

def parse_input(inputfile):
    ns = NameSpace()
    f = open(inputfile, 'r')
    fstr = f.read()
    ns.readdir = get_dir('READDIR', fstr)
    ns.writedir = get_dir('WRITEDIR', fstr)
    ns.camid = get_attr('ID', fstr) # id is a keyword
    ns.year = get_attr('YEAR', fstr)
    ns.month = get_attr('MONTH', fstr)
    ns.day = get_attr('DAY', fstr)
    ns.hour = get_attr('HOUR', fstr)
    ns.mnt = get_attr('MINUTE', fstr) # min is a keyword
    ns.sec = get_attr('SECOND', fstr)
    return ns

def retrieve_images(f_ns):
    if (not os.path.exists(f_ns.writedir)):
        os.makedirs(f_ns.writedir)

    filelist = os.listdir(f_ns.readdir)
    tot = len(filelist)
    cur = 0
    for filename in filelist:
        print_progress(cur, tot)
        cur += 1
        if filename.endswith('.jpg') or filename.endswith('.png'):
            img_ns = get_img_info(filename)
            f_dict = f_ns.__dict__
            img_dict = img_ns.__dict__
            for attr in img_dict:
                add_image = True
                if (f_dict[attr].lb is not None and \
                    f_dict[attr].lb > img_dict[attr]):
                    add_image = False
                elif (f_dict[attr].ub is not None and \
                      f_dict[attr].ub < img_dict[attr]):
                    add_image = False
                elif (f_dict[attr].ex is not None and \
                      f_dict[attr].ex != img_dict[attr]):
                    add_image = False
                elif (f_dict[attr].intv is not None and \
                      img_dict[attr] % f_dict[attr].intv != 0):
                    add_image = False
                if (add_image):
                    src = os.path.join(f_ns.readdir, filename)
                    dest = os.path.join(f_ns.writedir, filename)
                    shutil.copyfile(src, dest)
    print_progress(1, 1)
    sys.stdout.write('\n')
    return

def get_dir(name, fstr):
    m = re.search(re.escape(name) + r' *= *(\S*)\n', fstr)
    if m.group(1):
        return m.group(1)
    raise Exception('Could not find required field {0:s}'\
                    .format(name))
    
def get_attr(name, fstr):
    attr = NameSpace()
    m = re.search(re.escape(name) + r'_RANGE *= *(\S*)\n', fstr)
    if m.group(1):
        rngstr = m.group(1)
        m = re.search(r'(.*),(.*)', rngstr)
        if m:
            # upper bound and/or lower bound provided
            attr.ex = None
            if m.group(1):
                attr.lb = int(m.group(1))
            else:
                attr.lb = None
            if m.group(2):
                attr.ub = int(m.group(2))
            else:
                attr.ub = None
        else:
            # an exact value has been provided
            attr.ex = int(rngstr)
            attr.lb = None
            attr.ub = None
    else:
        attr.lb = None
        attr.ub = None
        attr.ex = None
    m = re.search(re.escape(name) + r'_INTERVAL *= *(\S*)\n', fstr)
    if m.group(1):
        attr.intv = int(m.group(1))
    else:
        attr.intv = None
    return attr

def print_progress(cur, tot):
    percent = float(cur) * 100 / tot
    # use sys.stdout.write instead of print so the code is compatible with
    # both python 2 and 3
    sys.stdout.write('\rPercent Complete: {0:0.2f}% '.format(percent))
    sys.stdout.flush()
    
def main(args):
    args_ns = parse_args(args)
    if (args_ns.read is not None):
        # A image subset will be created
        f_ns = parse_input(args_ns.read)
        retrieve_images(f_ns)
    else:
        # A template file will be created
        create_template(args_ns.create)
    
if __name__ == "__main__":
    main(sys.argv[1:])
