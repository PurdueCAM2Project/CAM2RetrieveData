def convert(val):
    fd4 = val % 256
    val = val / 256
    fd3 = val % 256
    val = val / 256
    fd2 = val % 256
    val = val / 256
    fd1 = val
    ipaddr = str(fd1) + "." + str(fd2) + "." + str(fd3) + "." + str(fd4)
    # print ipaddr
    return ipaddr
