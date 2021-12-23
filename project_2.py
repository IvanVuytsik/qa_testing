import os
from os import walk
import time
from dirsync import sync
import logging


# uncomment below for console/static input
#---------------------------------------------------------------------------
source = input('Indicate path to source catalogue: ')   # example - source
target = input('Indicate path to target catalogue: ')   # example - target
timer = int(input('Please provide interval: ')) # example - 5
log_path = input('Please path to save log: ')   # example - project_2.log

# source = 'source'
# target = 'target'
# timer = 5
# log_path = 'project_2.log'
#---------------------------------------------------------------------------
logger = logging.getLogger('project_2.py')
logger.setLevel(level=logging.DEBUG)
fh_a = logging.StreamHandler()
fh_b = logging.FileHandler(log_path)
fh_formatter = logging.Formatter('%(asctime)s %(levelname)s %(lineno)d:%(filename)s(%(process)d) - %(message)s')
fh_a.setFormatter(fh_formatter)
logger.addHandler(fh_a)
fh_b.setFormatter(fh_formatter)
logger.addHandler(fh_b)

#---------------------------------------------------------------------------
def auto_sync(source,target):
    sync(source,target,"sync",verbose=True, logger=logger)
#---------------------------------------------------------------------------
mtime, oldmtime = None, None
while True:
    mtime = os.path.getmtime(source)
    #------------------------auto sync dirs every interval------------------
    #auto_sync(source, target)
    #------------------------sync dirs when source changed------------------
    if mtime != oldmtime:
        sync(source,target,"sync",verbose=True, delete=True,logger=logger)
        oldmtime = mtime
        source_files = next(walk(source), (None, None, None))[2]
        target_files = next(walk(target), (None, None, None))[2]
        # -----------deletes files from target that do not match source-----
        for file in os.listdir(target):
            if file not in os.listdir(source):
                full_file_path = os.path.join(target, file)
                os.remove(full_file_path)
                print(f'Deleted files: {str(file)}')
        print(f'Source files: {str(source_files)}')
        print(f'Target files: {str(target_files)}')

        #---------------------logging--------------------
        with open(log_path, 'a') as f:
            f.write(f'Source files: {str(source_files)}')
            f.write(f'Target files: {str(target_files)}')
            f.write(f'Deleted files: {str(file)}')
    time.sleep(timer)



