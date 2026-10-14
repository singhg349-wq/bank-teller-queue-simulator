import contextlib
import io
import re
import unittest

from banking import Teller, banking_simulation


def run(commands):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        banking_simulation(commands)
    return out.getvalue()


def last_status(output):
    """Per-teller service time and idle % (later lines overwrite earlier ones)."""
    service = {m[0]: int(m[1]) for m in re.findall(r"Teller: (\d+) Total service time: (\d+)", output)}
    idle = {m[0]: float(m[1]) for m in re.findall(r"(\d+) idle time: ([\d.]+)%", output)}
    return service, idle


class TellerTests(unittest.TestCase):
    def test_service_returns_time_worked(self):
        t = Teller("0")
        t.accept(5)
        self.assertEqual(t.service(3), 3)
        self.assertEqual(t.service(3), 2)   # only 2 units left on this customer
        self.assertEqual(t.service(3), 0)   # nobody to serve
        self.assertEqual(t.get_total_service_time(), 5)
        self.assertTrue(t.is_available())


class SimulationTests(unittest.TestCase):
    def test_example_scenario(self):
        out = run(["call 3", "add 5 10 15", "service 6", "service 6", "status", "quit"])
        service, idle = last_status(out)
        self.assertEqual(service, {"0": 5, "1": 10, "2": 12})
        self.assertAlmostEqual(idle["0"], 58.33, places=2)
        self.assertAlmostEqual(idle["1"], 16.67, places=2)
        self.assertAlmostEqual(idle["2"], 0.0)

    def test_service_plus_idle_equals_elapsed_time(self):
        cycles = [4, 5, 3]
        out = run(["call 2", "add 3 8 2 7", *[f"service {c}" for c in cycles], "status", "quit"])
        service, idle = last_status(out)
        total = sum(cycles)
        for name in service:
            self.assertAlmostEqual(service[name] + idle[name] / 100 * total, total, places=1)

    def test_extra_spaces_are_ignored(self):
        out = run(["call   1", "add  4", "service 2 ", "status"])
        self.assertIn("Teller: 0 Total service time: 2", out)


if __name__ == "__main__":
    unittest.main()
