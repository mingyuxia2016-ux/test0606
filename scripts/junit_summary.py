import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def summarize_file(path: Path) -> str:
    if not path.exists():
        return f"### {path}\n\nReport file was not generated.\n"

    root = ET.fromstring(path.read_text(encoding="utf-8", errors="ignore"))
    suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))

    tests = sum(int(suite.attrib.get("tests", 0)) for suite in suites)
    failures = sum(int(suite.attrib.get("failures", 0)) for suite in suites)
    errors = sum(int(suite.attrib.get("errors", 0)) for suite in suites)
    skipped = sum(int(suite.attrib.get("skipped", 0)) for suite in suites)
    passed = tests - failures - errors - skipped

    lines = [
        f"### {path}",
        "",
        "| Total | Passed | Failed | Errors | Skipped |",
        "| ---: | ---: | ---: | ---: | ---: |",
        f"| {tests} | {passed} | {failures} | {errors} | {skipped} |",
        "",
    ]

    failed_cases = []
    for case in root.iter("testcase"):
        problem = case.find("failure") or case.find("error")
        if problem is not None:
            name = f"{case.attrib.get('classname', '')}.{case.attrib.get('name', '')}".strip(".")
            message = problem.attrib.get("message", "").replace("\n", " ")
            failed_cases.append((name, message[:300]))

    if failed_cases:
        lines.extend(["Failed cases:", ""])
        for name, message in failed_cases:
            lines.append(f"- `{name}`: {message}")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    report_paths = [Path(arg) for arg in sys.argv[1:]]
    if not report_paths:
        report_paths = [Path("reports/junit-base.xml"), Path("reports/junit-ai.xml")]

    print("# API Test Report\n")
    for path in report_paths:
        print(summarize_file(path))


if __name__ == "__main__":
    main()
