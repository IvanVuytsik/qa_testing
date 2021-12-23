from datetime import datetime
import psutil
import os
import json

def all_procs():
    list_pids = psutil.pids()
    for proc in psutil.process_iter(attrs=['pid', 'name', 'memory_percent']):
        try:
           #print(proc.info)
           open_files = len(proc.open_files())
           print(open_files)
        except psutil.AccessDenied:
              pass
        print("finished")

#-----------------------------------------------------------------------
def get_info(process, timer):
    pid = None
    for proc in psutil.process_iter():
        if process in proc.name():
            pid = f"ID: {proc.pid}"
            name = f"NAME: {proc.name()}"
            status = f"STATUS: {proc.status()}"
            started = f"STARTED: {datetime.fromtimestamp(proc.create_time())}"
            cpu = f"CPU: {proc.cpu_percent(interval=timer)}%"
            memory = f"MEMORY %: {proc.memory_percent():.1f}%"
            rss = f"RSS: {proc.memory_info().rss}"
            vms = f"VMS: {proc.memory_info().vms}"

            overview = proc.memory_full_info()

            proc_data = [(pid,name,status,started,cpu,memory, rss, vms)]
            #open_fd = len(psutil.Process().open_files())
            open_fd = len(proc.open_files())
            print("Open FDs: %d" % open_fd)
            print(proc_data)
            # print(overview) # uncomment / add to data for more data

#-------------------------------save-------------------------------
            data = {}
            data[f'{basename}'] = []
            data[f'{basename}'].append({'pid': pid,'name': name,'cpu': cpu,'memory': memory,
                                        'rss': rss, 'vms': vms,"open_fd": open_fd})
            with open('data.txt', 'a',) as outfile:
                json.dump(data, outfile,indent=1)

#-----------------------------------------------------------------
path = input("Please indicate path to .exe: ")
interval = int(input("Provide desired interval (sec): "))
basename = os.path.basename(path).split('.')[0]
# example:  C:\PyCharm Community Edition 2021.1.3\bin\pycharm64.exe

while True:
    get_info(basename, interval)
    #pass









