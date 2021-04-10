import sys
from Util import *

# List
def list_all(processes_):
    for p in processes_:
        print(p.list_m())

# Clock
def clock(processes_):
    for p in processes_:
        print(p.time_m())

# Kill
# Becomes buggy when bullying
def kill(processes_,pid):
    try:
        p = list(filter(lambda x: x.id == pid, processes_))[0]
    except:
        print("Such element does not exist")
        return processes_

    index = processes_.index(p)

    processes = processes_.copy()
    processes[index].isAlive = False

    if p.isCoordinator:
        processes = bully(processes)

    processes = [x for x in processes if x.id != pid]
    return processes

# Set Time
def set_time(processes_, pid, time):
    try:
        p = list(filter(lambda x: x.id == pid, processes_))[0]
    except:
        print("Such element does not exist")
        return


    index = processes_.index(p)
    processes = processes_.copy()
    coord_time = p.minutes() + p.difference

    # If coordinator, then send out the time difference to other processes
    if p.isCoordinator:
        p.time = time
        for proc in processes:
            if p.id != proc.id:
                proc.difference = p.minutes() - proc.minutes()
    else:
        p.time = time
        p.difference = coord_time - p.minutes()

    processes[index] = p
    return processes

def reload(processes_,input_loc):
    file = open(input_loc, "r")
    lines = file.readlines()
    file.close()
    processes = processes_.copy()
    for line in lines:
        tokens = line.split(",")
        id = tokens[0].strip()
        name = tokens[1].strip()
        time = tokens[2].strip()
        if len(list(filter(lambda x: x.id == id, processes))) == 0:
            processes.append(Process(id, name, time))

    processes = bully(processes)
    return processes


if __name__ == "__main__":
    # Entrypoint
    handle_argv(sys.argv,2)
    processes = bully(read_input(sys.argv[1]))
    choice = ""

    while choice!="exit":

        choice = input("\nPlease, enter your next action:\n").strip()
        # try:
        args = choice.split(" ")

        if args[0] == "exit":
            print("\nCiao")
        elif args[0] == "kill":
            if handle_argv(args,2):
                processes = kill(processes,args[1])
        elif args[0] == "list":
            list_all(processes)
        elif args[0] == "clock":
            clock(processes)
        elif args[0] == "set-time":
            if handle_argv(args,3):
                processes = set_time(processes,args[1],args[2])
        elif args[0] == "reload":
            processes = reload(processes,sys.argv[1])
        elif args[0] == "debug":
            print(processes)


        # except:
        #     print("Please try again")