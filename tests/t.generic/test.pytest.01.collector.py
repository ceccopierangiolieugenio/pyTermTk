import pytest

class ResultCollector:
    def __init__(self):
        self.results = []

    def pytest_runtest_logreport(self, report):
        if report.when == "call":
            self.results.append({
                "nodeid": report.nodeid,
                "outcome": report.outcome,
                "duration": report.duration,
                "longrepr": str(report.longrepr) if report.failed else None
            })

    def pytest_itemcollected(self, item):
        # Called during --collect-only
        self.results.append({
            "nodeid": item.nodeid,
            "outcome": "collected",
            "duration": 0,
            "longrepr": None
        })

def run_tests_and_collect():
    collector = ResultCollector()
    pytest.main(["-p no:terminal", "tests/"], plugins=[collector])
    return collector.results

def run_tests_and_collect_2():
    collector = ResultCollector()
    pytest.main(["--collect-only", "-p no:terminal", "tests/"], plugins=[collector])
    return collector.results

if __name__ == "__main__":
    results = run_tests_and_collect()
    for r in results:
        print(f"{r['nodeid']}: {r['outcome']} ({r['duration']:.2f}s)")
        if r['outcome'] == 'failed':
            print("  ↳ Error:", r['longrepr'])

    print("##################")

    results = run_tests_and_collect_2()
    for r in results:
        print(f"{r['nodeid']}")
        if r['outcome'] == 'failed':
            print("  ↳ Error:", r['longrepr'])
