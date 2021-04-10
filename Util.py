from Process import Process
import random

def handle_argv(argv, needed):
    if len(argv) < needed:
        print( "Not enough arguments supplied!")
        return False
    return True
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

def bully(processes):
    message_counter = 0

    current_process = random.randint(0,len(processes)-1)
    # Simulating the behaviour where process initiates bullying. The starting process cannot be dead
    while not processes[current_process].isAlive:
        current_process = random.randint(0, len(processes) - 1)

    # Random process, that initiates bullying
    current_process = processes[current_process]
    print(f"Process with id {current_process.id} initiated bullying")

    # An array of processes with higher IDs
    # We send all the messages to every element in "next" array.
    higher_ids = list(filter(lambda x: current_process.id < x.id, processes))
    message_counter+=len(higher_ids)

    while len(higher_ids) != 0:
        # After that we receive the response only from those, that are alive.
        higher_ids = list(filter(lambda x: x.isAlive, higher_ids))
        if len(higher_ids) == 0:
            break
        message_counter += len(higher_ids)
        # We find the smallest element from the list with ALIVE and HIGHER ID elements
        # This will be the element with the next id
        current_process = min(higher_ids,key=lambda x: x.id)
        # We again, send the messages to all the processes with higher IDs
        higher_ids = list(filter(lambda x: current_process.id < x.id, processes))
        message_counter += len(higher_ids)

    # At the end, send messages to all alive servers
    # New coordinator is elected and sends out the time difference
    for p in processes:
        if p.id == current_process.id:
            p.isCoordinator = True
            p.difference = 0
        else:

            p.isCoordinator = False
            # Coordinator sends the difference
            p.difference = current_process.minutes()-p.minutes()
        # Self-explanatory
        if not p.isFirst:
            p.increment_name()
        else:
            p.isFirst = False

    print(f"Process with id {current_process.id} is now the new coordinator")
    print("Total number of messages required to find coordinator:",message_counter+len(processes)-1)
    return processes

