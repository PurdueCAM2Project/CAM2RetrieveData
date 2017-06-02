import re
def convert(ipaddr):
    mch = re.search("(\d+)\.(\d+)\.(\d+)\.(\d+)", ipaddr)
    fd1 = mch.group(1)
    fd2 = mch.group(2)
    fd3 = mch.group(3)
    fd4 = mch.group(4)
    val = int(fd1)
    val = val * 256 + int(fd2)
    val = val * 256 + int(fd3)
    val = val * 256 + int(fd4)
    # print val
    return val
    
