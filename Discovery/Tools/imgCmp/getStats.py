import imgCmp
import sys
import re
import os
import cv2

def main(args):
    source_dir = args[0]
    f = open('{0:s}/results.csv'.format(source_dir), 'w')
    f.write('img1,img2,mean,median,std_dev,objects,time\n')
    dir_list = [x[0] for x in os.walk(source_dir)]
    for cur_dir in dir_list:
        if cur_dir != source_dir:
            obj_file = os.path.join(cur_dir, 'objects.csv')
            f_obj = open(obj_file, 'r')
            lines = f_obj.readlines()
            obj_dict = {}
            for line in lines:
                m = re.match(r'([\w\.\-]+),(\d+)', line)
                if m:
                    obj_dict[m.group(1)] = int(m.group(2))
            f_obj.close()
            for root, dirnames, filenames in os.walk(cur_dir):
                i = 0
                while (i < len(filenames) - 1):
                    if (filenames[i] == 'objects.csv'):
                        if (i < len(filenames) - 2):
                            i += 1
                        else:
                            break
                    img1 = os.path.join(root, filenames[i])
                    j = i + 1
                    while (j < len(filenames)):
                        if (filenames[j] == 'objects.csv'):
                            if (j < len(filenames) - 1):
                                j += 1
                            else:
                                break
                        img2 = os.path.join(root, filenames[j])
                        print('comparing {0:s} and {1:s}'.format(img1, img2))
                        diff_list = imgCmp.cmpMSE(cv2.imread(img1),\
                                           cv2.imread(img2))
                        mean = sum(diff_list) / len(diff_list)
                        median = imgCmp.getMedian(diff_list)
                        std_dev = imgCmp.getStdDev(diff_list, mean=mean)
                        if (filenames[i] in obj_dict and \
                            filenames[j] in obj_dict):
                            objs = obj_dict[filenames[i]] + \
                                   obj_dict[filenames[j]]
                        else:
                            objs = -1
                        f.write('{0:s},{1:s},{2:0.2f},{3:0.2f},'\
                                '{4:0.2f},{5:d}\n'\
                                .format(filenames[i], filenames[j],\
                                        mean, median, std_dev, objs))
                        j += 1
                    i += 1
                        

if __name__ == '__main__':
    main(sys.argv[1:])
