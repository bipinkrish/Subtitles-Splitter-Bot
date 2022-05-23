import psutil
import platform
from datetime import datetime
import cpuinfo
import socket
import uuid
import re

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}\n"
        bytes /= factor

def System_information():
    with open("./info.txt", "w")as file:
        file.write("==== System Information ====\n")
        uname = platform.uname()
        file.write(f"System: {uname.system}\n")
        file.write(f"Node Name: {uname.node}\n")
        file.write(f"Release: {uname.release}\n")
        file.write(f"Version: {uname.version}\n")
        file.write(f"Machine: {uname.machine}\n")
        file.write(f"Processor: {uname.processor}\n")
        file.write(f"Processor: {cpuinfo.get_cpu_info()['brand_raw']}\n")
        file.write(f"Ip-Address: {socket.gethostbyname(socket.gethostname())}\n")
        file.write(f"Mac-Address: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}\n")


        # Boot Time
        file.write("==== Boot Time ====\n")
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        file.write(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}\n")


        # file.write CPU information
        file.write("==== CPU Info ====\n")
        # number of cores
        file.write(f"Physical cores:{psutil.cpu_count(logical=False)}\n")
        file.write(f"Total cores:{psutil.cpu_count(logical=True)}\n" )
        # CPU frequencies
        cpufreq = psutil.cpu_freq()
        file.write(f"Max Frequency: {cpufreq.max:.2f}Mhz\n")
        file.write(f"Min Frequency: {cpufreq.min:.2f}Mhz\n")
        file.write(f"Current Frequency: {cpufreq.current:.2f}Mhz\n")
        # CPU usage
        file.write("CPU Usage Per Core:\n")
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            file.write(f"Core {i}: {percentage}%\n")
        file.write(f"Total CPU Usage: {psutil.cpu_percent()}%\n")


        # Memory Information
        file.write("==== Memory Information ====\n")
        # get the memory details
        svmem = psutil.virtual_memory()
        file.write(f"Total: {get_size(svmem.total)}")
        file.write(f"Available: {get_size(svmem.available)}")
        file.write(f"Used: {get_size(svmem.used)}")
        file.write(f"Percentage: {svmem.percent}%\n")



        file.write("== SWAP ==\n")
        # get the swap memory details (if exists)
        swap = psutil.swap_memory()
        file.write(f"Total: {get_size(swap.total)}")
        file.write(f"Free: {get_size(swap.free)}")
        file.write(f"Used: {get_size(swap.used)}")
        file.write(f"Percentage: {swap.percent}%\n")



        # Disk Information
        file.write("==== Disk Information ====\n")
        file.write("Partitions and Usage:")
        # get all disk partitions
        partitions = psutil.disk_partitions()
        for partition in partitions:
            file.write(f"Device: {partition.device} \n")
            file.write(f"Mountpoint: {partition.mountpoint}\n")
            file.write(f"File system type: {partition.fstype}\n")
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                # this can be catched due to the disk that
                # isn't ready
                continue
            file.write(f"Total Size: {get_size(partition_usage.total)}")
            file.write(f"Used: {get_size(partition_usage.used)}")
            file.write(f"Free: {get_size(partition_usage.free)}")
            file.write(f"Percentage: {partition_usage.percent}%\n")
            break
            
        # get IO statistics since boot
        file.write("==== IO statistics since boot ====\n")
        disk_io = psutil.disk_io_counters()
        file.write(f"Total read: {get_size(disk_io.read_bytes)}")
        file.write(f"Total write: {get_size(disk_io.write_bytes)}")

        ##get IO statistics since boot
        net_io = psutil.net_io_counters()
        file.write(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
        file.write(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")



    
