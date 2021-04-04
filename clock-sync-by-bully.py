import sys
import random

class Process:
    def __init__(self,id,name,time,isCoordinator = False, isAlive = True):
        self.id = id
        self.name = name
        self.time = time
        self.isCoordinator = isCoordinator
        self.isAlive = isAlive

    # DEBUG purpose
    def __str__(self):
        return f"{{ name: {self.name}, id:{self.id}, time:{self.time}, isCoordinator:{self.isCoordinator}, isAlive:{self.isAlive}}}"

    def list_m(self):
        if self.isCoordinator:
            return f"{self.id}, {self.name}, (Coordinator)"
        else:
            return f"{self.id}, {self.name}"

    def increment_name(self):
        old_name = self.name.split("_")
        old_name[1] = str((int(old_name[1])+1))
        self.name = "_".join(old_name)

    def __repr__(self):
        return self.__str__()

# Helper to handle arguments
def handle_argv(argv, needed):
    if len(argv) < needed:
        print( "Not enough arguments supplied!")
        exit(-1)

# Read input file and load the program
def read_input(input_loc):
    file = open(input_loc,"r")
    processes = []
    lines = file.readlines()
    file.close()

    for line in lines:
        tokens = line.split(",")
        id = tokens[0].strip()
        name = tokens[1].strip()
        time = tokens[2].strip()
        processes.append(Process(id,name,time))

    return processes

# List
def list_all(processes):
    for p in processes:
        print(p.list_m())

def bully(processes, isFirst):
    message_counter = 0
    current_process = random.randint(0,len(processes)-1)
    # Random process, that initiates bullying
    current_process = processes[current_process]
    # An array of processes with higher IDs
    # We send all the messages to every element in "next" array.
    higher_ids = list(filter(lambda x: current_process.id < x.id, processes))
    message_counter+=len(higher_ids)

    while len(higher_ids) != 0:
        # After that we receive the response only from those, that are alive.
        higher_ids = list(filter(lambda x: x.isAlive, higher_ids))
        message_counter += len(higher_ids)
        # We find the smallest element from the list with ALIVE and HIGHER ID elements
        # This will be the element with the next id
        current_process = min(higher_ids,key=lambda x: x.id)
        # We again, send the messages to all the processes with higher IDs
        higher_ids = list(filter(lambda x: current_process.id < x.id, processes))
        message_counter += len(higher_ids)

    # At the end, send messages to all alive servers
    # New coordinator is elected
    for p in processes:
        if p.id == current_process.id:
            p.isCoordinator = True
        else:
            p.isCoordinator = False
        # Self-explanatory
        if not isFirst: p.increment_name()

    # TODO: Clock synchronization logic
    print(f"Process with id {current_process.id} is now the new coordinator")
    print("Total number of messages required to find coordinator:",message_counter+len(processes)-1)
    return processes



if __name__ == "__main__":
    # Entrypoint
    handle_argv(sys.argv,2)
    processes = read_input(sys.argv[1])

    processes = bully(processes,True)
