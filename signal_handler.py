class ProgramKilled(Exception):
    print("Program was killed.")
    pass

def signal_handler(signum, frame):
    raise ProgramKilled