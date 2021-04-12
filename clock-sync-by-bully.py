import sys
import util
from process import Process
from ticker import Ticker


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
def kill(processes_, pid):
    if not util.can_kill_or_freeze(processes_):
        print("Can't kill the last process")
        return processes_

    try:
        p = list(filter(lambda x: x.id == pid, processes_))[0]
    except:
        print("Such element does not exist")
        return processes_

    index = processes_.index(p)

    processes = processes_.copy()
    processes[index].isAlive = False
    # kill the ticking clock
    processes[index].ticket_minutes = 0

    # first remove from the list
    processes = [x for x in processes if x.id != pid]
    # then select new coordinator
    if p.isCoordinator:
        processes = util.bully(processes)

    return processes


# Set Time
# if the time of any other process is changed, then that process should be synchronized again based on the
# time of the coordinator.
def set_time(processes_, pid, time):
    try:
        p = list(filter(lambda x: x.id == pid and not x.isFrozen, processes_))[0]
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
            proc.ticked_minutes = 0
            if p.id != proc.id:
                proc.difference = p.minutes() - proc.minutes()
    else:
        p.time = time
        p.difference = coord_time - p.minutes()

    processes[index] = p
    return processes


def freeze(processes_, id):
    if not util.can_kill_or_freeze(processes_):
        print("Can't freeze the last process")
        return

    p = list(filter(lambda x: x.id == id, processes_))[0]

    index = processes_.index(p)

    processes_[index].isFrozen = True

    if p.isCoordinator:
        util.bully(processes_)


def unfreeze(processes_, id):
    try:
        p = list(filter(lambda x: x.id == id, processes_))[0]
    except:
        print("Such element does not exist")

    index = processes_.index(p)

    if not processes_[index].isFrozen:
        print("This process is not frozen")
        return processes_

    processes = processes_.copy()

    processes[index].isFrozen = False
    # From desc:
    # Once it becomes the
    # coordinator, it uses its default clock as the new time (the time from the process_file).
    processes[index].ticket_minutes = 0
    current_coordinator = list(filter(lambda x: x.isCoordinator, processes))[0]

    if id > current_coordinator.id:
        util.bully(processes, entry_idx=index)
    else:
        processes[index].ticked_minutes = current_coordinator.ticked_minutes
        processes[index].difference = current_coordinator.minutes() - processes[index].minutes()

    return processes


def reload(processes_, input_loc):
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

    processes = util.bully(processes)
    return processes


if __name__ == "__main__":
    # Entrypoint
    util.handle_argv(sys.argv, 2)
    processes = util.bully(util.read_input(sys.argv[1]))
    choice = ""
    ticker = Ticker(processes)
    ticker.start()

    while choice != "exit":
        try:
            choice = input("\nPlease, enter your next action:\n").strip()
            args = choice.split(" ")

            if args[0] == "exit":
                print("\nCiao")
            elif args[0] == "kill":
                if util.handle_argv(args, 2):
                    processes = kill(processes, args[1])
            elif args[0] == "list":
                list_all(processes)
            elif args[0] == "clock":
                clock(processes)
            elif args[0] == "set-time":
                if util.handle_argv(args, 3):
                    processes = set_time(processes, args[1], args[2])
            elif args[0] == "freeze":
                if util.handle_argv(args, 2):
                    freeze(processes, args[1])
            elif args[0] == "unfreeze":
                if util.handle_argv(args, 2):
                    processes = unfreeze(processes, args[1])
            elif args[0] == "reload":
                processes = reload(processes, sys.argv[1])
                ticker.upd_list(processes)
            elif args[0] == "debug":
                print(processes)
            else:
                print('Unsupported command')

        except KeyboardInterrupt:
            print("Please, do not use Ctrl+C. Try again with \'exit\' command")
        except:
            print("Please try again")
    ticker.stop()
