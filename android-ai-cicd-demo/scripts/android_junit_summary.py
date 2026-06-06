import sys
import xml.etree.ElementTree as ET
from pathlib import Path


DEFAULT_REPORT_DIRS = [
    Path("app/build/test-results/testDebugUnitTest"),
    Path("app/build/outputs/androidTest-results/connected/debug"),
]


def summarize_report(path: Path) -> tuple[int, int, int, int, list[str]]:
    root = ET.fromstring(path.read_text(encoding="utf-8", errors="ignore"))
    tests = int(root.attrib.get("tests", 0))
    failures = int(root.attrib.get("failures", 0))
    errors = int(root.attrib.get("errors", 0))
    skipped = int(root.attrib.get("skipped", 0))

    failed_cases = []
    for case in root.iter("testcase"):
        problem = case.find("failure")
        if problem is None:
            problem = case.find("error")
        if problem is not None:
            name = f"{case.attrib.get('classname', '')}.{case.attrib.get('name', '')}".strip(".")
            message = problem.attrib.get("message", "").replace("\n", " ")
            failed_cases.append(f"- `{name}`: {message[:300]}")

    return tests, failures, errors, skipped, failed_cases


def print_summary(title: str, reports: list[Path]) -> None:
    print(f"## {title}\n")

    if not reports:
        print("没有找到测试报告。\n")
        return

    total = failures = errors = skipped = 0
    failed_cases = []
    for report in reports:
        tests, report_failures, report_errors, report_skipped, report_failed_cases = summarize_report(report)
        total += tests
        failures += report_failures
        errors += report_errors
        skipped += report_skipped
        failed_cases.extend(report_failed_cases)

    passed = total - failures - errors - skipped
    print("| Total | Passed | Failed | Errors | Skipped |")
    print("| ---: | ---: | ---: | ---: | ---: |")
    print(f"| {total} | {passed} | {failures} | {errors} | {skipped} |\n")

    if failed_cases:
        print("失败用例：\n")
        print("\n".join(failed_cases))
        print()


def main() -> None:
    report_dirs = [Path(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else DEFAULT_REPORT_DIRS

    print("# Android APK 构建与测试报告\n")
    for report_dir in report_dirs:
        reports = sorted(report_dir.glob("TEST-*.xml"))
        print_summary(str(report_dir), reports)


if __name__ == "__main__":
    main()
