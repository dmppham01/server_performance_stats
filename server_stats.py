import subprocess

def get_cpu_usage():
    # Get CPU usage from top command
    try:
        output = subprocess.check_output(["top", "-bn1"], universal_newlines=True)
        for line in output.splitlines():
            if "Cpu(s)" in line:
                return line.strip()
    except Exception as e:
        return f"Error fetching CPU usage: {e}"

def get_memory_usage():
    # Get memory usage from free command
    try:
        output = subprocess.check_output(["free", "-m"], universal_newlines=True)
        lines = output.splitlines()
        mem_line = lines[1].split()
        total, used, free = int(mem_line[1]), int(mem_line[2]), int(mem_line[3])
        percent_used = (used / total) * 100
        return f"Memory Usage: {used} MB Used / {total} MB Total ({percent_used:.2f}% used)"
    except Exception as e:
        return f"Error fetching memory usage: {e}"

def get_disk_usage():
    # Get disk usage from df command
    try:
        output = subprocess.check_output(["df", "-h", "/"], universal_newlines=True)
        lines = output.splitlines()
        root_line = lines[1].split()
        filesystem, size, used, available, percent_used, mount = root_line
        return f"Disk Usage: {used} Used / {size} Total ({percent_used} used)"
    except Exception as e:
        return f"Error fetching disk usage: {e}"

def get_top_processes(sort_by, count=5):
    # Get top processes by CPU or memory usage
    try:
        if sort_by == "cpu":
            sort_field = 2  # The %CPU field in the ps aux output
        elif sort_by == "mem":
            sort_field = 3  # The %MEM field in the ps aux output
        else:
            return "Invalid sort criteria"

        # Run the ps command and pipe it through sort and head
        output = subprocess.check_output(
            f"ps aux --sort=-%{sort_by} | head -n {count + 1}",
            shell=True,
            universal_newlines=True
        )

        return output.strip()
    except Exception as e:
        return f"Error fetching top processes by {sort_by}: {e}"

def get_system_info():
    try:
        # OS version
        os_info = subprocess.check_output(["uname", "-a"], universal_newlines=True).strip()
        # Uptime
        uptime = subprocess.check_output(["uptime", "-p"], universal_newlines=True).strip()
        # Load average
        load_avg = subprocess.check_output(["uptime"], universal_newlines=True).split("load average:")[1].strip()
        return f"OS Info: {os_info}\nUptime: {uptime}\nLoad Average: {load_avg}"
    except Exception as e:
        return f"Error fetching system info: {e}"

def main():
    print("=== Server Performance Stats ===")
    print(get_cpu_usage())
    print(get_memory_usage())
    print(get_disk_usage())
    print("\nTop 5 Processes by CPU Usage:")
    print(get_top_processes("cpu"))
    print("\nTop 5 Processes by Memory Usage:")
    print(get_top_processes("mem"))
    print("\n=== System Information ===")
    print(get_system_info())

if __name__ == "__main__":
    main()
