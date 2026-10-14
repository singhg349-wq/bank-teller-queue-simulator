# Bank Teller Queue Simulator

![tests](https://github.com/singhg349-wq/bank-teller-queue-simulator/actions/workflows/tests.yml/badge.svg)

A discrete-time simulation of a multi-teller bank in Python. Customers wait in one shared queue, tellers serve them in fixed time cycles, and the simulation tracks how much of each teller's time went to serving customers and how much was idle.

## Commands

The simulation is driven by a small command language:

| Command | What it does |
|---|---|
| `call N` | Creates `N` tellers, numbered `0` to `N-1` |
| `add t1 t2 ...` | Adds customers to the back of the queue, each needing the given units of service |
| `service N` | Advances time by `N` units: each free teller takes the next customer in line, then every teller works up to `N` units on their customer |
| `status` | Prints each teller's total service time, the queue length, and each teller's idle time as a percentage of all elapsed time |
| `quit` | Ends the simulation and prints a final summary |

## Running

```bash
python3 banking.py                        # built-in example scenario
python3 banking.py example_commands.txt   # commands from a file, one per line
python3 banking.py - < my_commands.txt    # commands from standard input
```

Only the standard library is needed.

## Example

`example_commands.txt` (also the built-in scenario):

```
call 3
add 5 10 15
service 6
status
service 6
status
quit
```

Output:

```
Teller: 0 Total service time: 5
Teller: 1 Total service time: 6
Teller: 2 Total service time: 6
Customers waiting in queue: 0
0 idle time: 16.67%
1 idle time: 0.00%
2 idle time: 0.00%
Teller: 0 Total service time: 5
Teller: 1 Total service time: 10
Teller: 2 Total service time: 12
Customers waiting in queue: 0
0 idle time: 58.33%
1 idle time: 16.67%
2 idle time: 0.00%
Simulation ended.
Teller: 0 Total service time: 5
Teller: 1 Total service time: 10
Teller: 2 Total service time: 12
```

Teller 0 finishes its 5-unit customer one unit into the first 6-unit cycle, then has nobody to serve in the second cycle: 7 idle units out of 12, or 58.33%.

## How it works

This is a multi-server, single-queue system: several tellers pull from one shared FIFO line instead of each having their own. Time moves in discrete cycles, so each `service N` represents `N` units passing at once.

For every teller in every cycle, `Teller.service()` returns how many units were actually spent serving, and the rest of the cycle counts as idle. Idle percentage is total idle time divided by total elapsed time, so it covers the whole run, not just the latest cycle. For every teller, service time plus idle time always equals elapsed time, and the tests check that.

## Design notes

- **Manual command parsing:** commands are split into tokens with a hand-written character loop instead of `str.split()`. It behaves the same for this input, extra spaces included, but shows the tokenizing logic explicitly.
- **Partial-cycle idle time:** a teller who finishes a customer partway through a cycle is idle only for the remainder of that cycle, not the whole cycle.
- **Same-cycle pickup:** a free teller takes a new customer at the start of a `service` cycle and starts on them in that same cycle, so no customer waits an extra cycle for an open teller.
- **`queue.Queue`:** it's thread-safe, which this single-threaded simulation doesn't need (`collections.deque` would also work). It was chosen for its FIFO semantics and clean `get_nowait()` / `Empty` handling.

## Tests

```bash
python3 -m unittest -v
```

The tests run automatically on every push through GitHub Actions.

## License

MIT

## Author

Gurshmeer Singh
