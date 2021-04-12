# Process manager with Bullying and Berkeley algorithms


`python3 clock-by-bully.py input.txt` - use this command to start the application.

**NB!** Clocks go up by one minute every 5 seconds.

### How to move around:

Once you have started an application, you will be asked for commands. 
Their meaning is as follows:

`list` - lists all the processes with their IDs and names.

`clock` - lists all the processes with their names and times.

`kill <pid>` - kills a process with the specified process id.

`set-time <pid> <(h)h:(m)m>` - sets a new personal time to a process. Note that it will be personal time,
so if the coordinator's value is still present, it will not be visible unless this
process becomes a coordinator itself.

`freeze <pid>` - freezes the process.

`unfreeze <pid>` - unfreezes the process.

`reload` - reloads the input file and if necessary updates the processes array. 

#### Extra:

At any time it is possible to see the full state of each individual process with 
`debug` command, that prints a list of processes with their attributes.
