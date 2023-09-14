import psutil
import time
from subprocess import call
from prettytable import PrettyTable

def increasePriority():
	pid = int(input("pid: "))
	process = psutil.Process(pid)
	priority = process.nice()
	print(f"Current priority of process {pid} is {priority}")
	priority += int(input("Increase by?: "))
	print(f"Increasing priority of {pid} to {priority}")
	process.nice(priority)
	time.sleep(2)

def decreasePriority():
	pid = int(input("pid: "))
	process = psutil.Process(pid)
	priority = process.nice()
	print(f"Current priority of process {pid} is {priority}")
	priority -= int(input("Decrease by?: "))
	print(f"Decreasing priority of {pid} to {priority}")
	process.nice(priority)
	time.sleep(2)

def killProcess():
	pid = int(input("pid: "))
	print(f"Killing process {pid}")
	process = psutil.Process(pid) 
	process.kill()
	time.sleep(2)

# Run an infinite loop to constantly monitor the system
while True:
	# Clear the screen using a bash command
	call('clear')
 
	print("==============================Process Monitor\
	======================================")
 
	# Fetch the battery information
	battery = psutil.sensors_battery().percent
	print("----Battery Available: %d " % (battery,) + "%\n")
 

	print("----Processes----")
	process_table = PrettyTable(['PID', 'PNAME', 'STATUS',
								 'CPU', 'NUM THREADS', 'MEMORY(MB)', 'PRIORITY'])
 
	proc = []
	# get the pids 
	for pid in psutil.pids():
		try:
			p = psutil.Process(pid)
			# trigger cpu_percent() the first time which leads to return of 0.0
			p.cpu_percent()
			proc.append(p)

		except Exception as e:
			pass

	# sort by cpu_percent
	top = {}
	for p in proc:
		# trigger cpu_percent() the second time for measurement
		try:
			top[p] = p.cpu_percent()
		except:
			top[p] = 0


	top_list = sorted(top.items(), key=lambda x: x[1])
	
	top_list.reverse()
 
	for p, cpu_percent in top_list[:30]:
		# While fetching the processes, some of the subprocesses may exit 
		# Hence we need to put this code in try-except block
		try:
			# oneshot to improve info retrieve efficiency
			with p.oneshot():
				process_table.add_row([
					str(p.pid),
					p.name(),
					p.status(),
					f'{cpu_percent:.2f}' + "%",
					p.num_threads(),
					f'{p.memory_info().rss / 1e6:.3f}',
					p.nice()
				])
 
		except Exception as e:
			pass
	print(process_table)
 

	print("1) Continue")
	print("2) Increase Priority")
	print("3) Decrease Priority")
	print("4) Kill Process")
	print("5) Exit")
	option = int(input("Enter option: "))
	if option == 1:
		continue
	elif option == 2:
		increasePriority()
	elif option == 3:
		decreasePriority()
	elif option == 4:
		killProcess()
	elif option==5:
		exit()