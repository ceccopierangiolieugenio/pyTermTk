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

def run_tests_and_collect():
    collector = ResultCollector()
    pytest.main(["tests/"], plugins=[collector])
    return collector.results

def run_tests_and_collect_2():
    collector = ResultCollector()
    pytest.main(["--collect-only", "-q", "tests/"], plugins=[collector])
    return collector.results

if __name__ == "__main__":
    results = run_tests_and_collect()
    for r in results:
        print(f"{r['nodeid']}: {r['outcome']} ({r['duration']:.2f}s)")
        if r['outcome'] == 'failed':
            print("  ↳ Error:", r['longrepr'])

    print()

    results = run_tests_and_collect_2()
    for r in results:
        print(f"{r['nodeid']}: {r['outcome']} ({r['duration']:.2f}s)")
        if r['outcome'] == 'failed':
            print("  ↳ Error:", r['longrepr'])
