class Process:
    def __init__(self,id,name,time,isCoordinator = False, isAlive = True, difference=0):
        self.id = id
        self.name = name
        self.time = time
        self.isCoordinator = isCoordinator
        self.isAlive = isAlive
        self.difference = difference
        self.isFirst = True

    # DEBUG purpose
    def __str__(self):
        return f"\n{{ \n\tname: {self.name}, \n\tid:{self.id}, " \
               f"\n\ttime:{self.time}, \n\tisCoordinator:{self.isCoordinator}, " \
               f"\n\tisAlive:{self.isAlive}\n\tdifference:{self.difference}" \
               f"\n\tisFirst:{self.isFirst}}}"

    def __repr__(self):
        return self.__str__()

    def list_m(self):
        if self.isCoordinator:
            return f"{self.id}, {self.name}, (Coordinator)"
        else:
            return f"{self.id}, {self.name}"

    def time_m(self):
        return f"{self.name}, {self.clock()}"

    def set_time(self, time):
        self.time = time


    def increment_name(self):
        old_name = self.name.split("_")
        old_name[1] = str((int(old_name[1])+1))
        self.name = "_".join(old_name)

    def minutes(self):
        hours,minutes = self.time.split(":")
        return int(hours)*60 + int(minutes)

    def clock(self):
        coord_time = self.difference + self.minutes()
        hours = str(coord_time//60)
        minutes = str(coord_time%60)
        if len(hours) == 1:
            hours = "0"+hours
        if len(minutes) == 1:
            minutes = "0"+minutes

        return f"{hours}:{minutes}"



