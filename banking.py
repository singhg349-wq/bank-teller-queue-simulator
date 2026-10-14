
#Author - Gurshmeer Singh

from queue import Queue, Empty

class Teller:
    def __init__(self, name):
        #Initialize a teller .
        self.name = name
        self.total_service_time = 0
        self.current_customer_time = None

    def get_name(self):
        return self.name

    def __str__(self):
        return f"Teller: {self.name} Total service time: {self.total_service_time}"

    def service(self, serv_time):
        #Serve a customer for a given amount of time.
        #Returns how many of those time units were actually spent working.
        if self.current_customer_time is None:
            return 0
        if serv_time >= self.current_customer_time:
            worked = self.current_customer_time
            self.current_customer_time = None
        else:
            worked = serv_time
            self.current_customer_time -= serv_time
        self.total_service_time += worked
        return worked

    def accept(self, cust_time):
        #Accept a new customer with their requested time if available.
        if self.current_customer_time is None:
            self.current_customer_time = cust_time

    def get_total_service_time(self):
        return self.total_service_time

    def make_available(self):
        #Make the teller available for a new customer.
        self.current_customer_time = None

    def is_available(self):
        return self.current_customer_time is None


def banking_simulation(commands):
    #Simulate the bank service system based on given commands.
    tellers = []
    queue = Queue()
    total_time = 0
    idle_times = {}
    for command in commands:
        # Manually splitting the command instead of using split()
        parts = []
        temp = ""
        for char in command:
            if char == " ":
                if temp:
                    parts.append(temp)
                    temp = ""
            else:
                temp += char
        if temp:  # append last part if there was no space at the end
            parts.append(temp)

        if not parts:  # Skip empty commands
            continue
        action = parts[0]

        if action == "call":
            num_tellers = int(parts[1])
            tellers = [Teller(str(i)) for i in range(num_tellers)]
            idle_times = {teller.get_name(): 0 for teller in tellers}

        elif action == "add":
            for time in map(int, parts[1:]):
                queue.put(time)

        elif action == "service":
            cycle_time = int(parts[1])
            for teller in tellers:
                if teller.is_available() and not queue.empty():
                    try:
                        teller.accept(queue.get_nowait())
                    except Empty:
                        pass
                worked = teller.service(cycle_time)
                # Idle = the part of this cycle the teller wasn't serving anyone
                idle_times[teller.get_name()] += cycle_time - worked
            total_time += cycle_time

        elif action == "status":
            for teller in tellers:
                print(teller)
            print(f"Customers waiting in queue: {queue.qsize()}")
            for teller in tellers:
                if total_time > 0:
                    idle_percentage = (idle_times[teller.get_name()] / total_time) * 100
                else:
                    idle_percentage = 0
                print(f"{teller.get_name()} idle time: {idle_percentage:.2f}%")

        elif action == "quit":
            print("Simulation ended.")
            for teller in tellers:
                print(teller)


# Example commands, used when no command file is given
EXAMPLE_COMMANDS = [
    "call 3",  # Create 3 tellers (t0, t1, t2)
    "add 5 10 15",  # Add 3 customers with service times 5, 10, and 15
    "service 6",  # Run a service cycle of 6 units of time
    "status",  # Print the status of the tellers and the queue
    "service 6",  # Run another service cycle of 6 units of time
    "status",  # Print the status again
    "quit"  # End the simulation
]


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # Read commands from a file, one per line ("-" means standard input)
        source = sys.stdin if sys.argv[1] == "-" else open(sys.argv[1])
        commands = [line.strip() for line in source if line.strip()]
    else:
        commands = EXAMPLE_COMMANDS
    banking_simulation(commands)
