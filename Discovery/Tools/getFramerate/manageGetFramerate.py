import getFramerate
import sys
import os
import re
import error

def main(args):
    try:
        assert len(args) == 2
        folder_to_load = args[1]
    except Exception as e:
        print("Input Folder Not Found.")
        print("Call Syntax:\n python manageGetFramerate.py <Input Directory> ")
        return

    files = os.listdir(folder_to_load)
    output = [] # List of all cameras in all files
    x = 0
    for onefile in files:
        if onefile.find(".txt") != -1:
                fInput = "{}{}".format(folder_to_load, onefile)
                print(fInput)
                onefile = re.search(r'(?P<filename>[^.]*)', onefile)
                duration = -1
                amountToProcess = 50
                camera_dump_threshold = 60*60
                is_video = 0

                DB_PASSWORD = ''

                for x in range(1,4):
                    results_path = "{}{}".format(onefile.group("filename"),x)
                    print("Pass: {}".format(x))
                    try:
                        getFramerate.setup(fInput, duration, amountToProcess, camera_dump_threshold, results_path, is_video, DB_PASSWORD)
                    except KeyboardInterrupt:
                        raise(KeyboardInterrupt)
                    except Exception, e:
                        print("Error: {}".format(e))

if __name__ == '__main__':
    main(sys.argv)