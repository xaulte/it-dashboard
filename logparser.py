# ── Application Metadata ──────────────────────────────────
APP_NAME = "SERVER LOG ANALYSIS REPORT"
VERSION = "0.1.0"
CREATOR_NAME = "Austin Windorski"
PROF_NAME = "Prof. Frank Mora"
COURSE_NAME = "COP1034C - Python for IT"

from datetime import date
today = date.today()
todaystr = today.isoformat()  # 'YYYY-MM-DD'

# Initialize
severity_counts = {}
unique_errors = set()
critical_events = set()
log_entries = []

# Parse and accumulate
def parse_line(line):
    # Basic parser; adjust regex to match your real log format
    # Example format: 2026-04-19 12:34:56 [ERROR] Something happened
    import re
    m = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(\w+)\] (.*)$', line)
    if not m:
        return None
    date_field, severity, message = m.groups()
    return {'date': date_field, 'severity': severity, 'message': message}

try:
    with open('server.log', 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            entry = parse_line(line)
            if not entry:
                continue  # skip lines that don’t parse

            severity = entry['severity']
            message = entry['message']
            date_field = entry['date']

            # Increment severity counter
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

            # Unique ERROR messages
            if severity == "ERROR":
                unique_errors.add(message)

            # CRITICAL events
            if severity == "CRITICAL":
                critical_events.add(message)

            # Append parsed entry
            log_entries.append({'date': date_field, 'severity': severity, 'message': message})
except FileNotFoundError:
    print("Error: server.log not found. Place the log file in the same directory as this script.")
    exit(1)

# Total lines
total_lines = len(log_entries)
error_count = severity_counts.get("ERROR", 0)
error_rate = (error_count / total_lines) * 100 if total_lines > 0 else 0.0

# Build list of ERROR entries
error_entries = [entry for entry in log_entries if entry['severity'] == "ERROR"]
print(f"Total errors found: {len(error_entries)}")

header_lines = []
for level in ["INFO", "WARNING", "ERROR", "CRITICAL"]:
    count = severity_counts.get(level, 0)
    header_lines.append(f"{level:<9}: {count:>4}")
header_section = "\n".join(header_lines)

bottom_unique_errors = ["UNIQUE ERROR MESSAGES", "=" * 36]
if unique_errors:
    bottom_unique_errors += [f"- {err}" for err in sorted(unique_errors)]
else:
    bottom_unique_errors += ["(none)"]

bottom_critical = ["UNIQUE CRITICAL MESSAGES", "=" * 36]
if critical_events:
    bottom_critical += [f"- {c}" for c in sorted(critical_events)]
else:
    bottom_critical += ["(none)"]

bottom_section = "\n".join(bottom_unique_errors)  # not used directly for header; shown separately below
critical_section = "\n".join(bottom_critical)
# Write the report
with open('log_summary.txt', 'w') as out:
    print("=" * 37, file=out)
    print(f"{APP_NAME} v{VERSION}", file=out)
    print(f"{CREATOR_NAME} | {PROF_NAME}", file=out)
    print(f"{COURSE_NAME} | {today}", file=out)
    print("=" * 37, file=out)
    print(header_section, file=out)
    print(f"\nError rate: {error_rate:.2f}%", file=out)
    print("Unique ERROR messages: {}".format(len(unique_errors)), file=out)
    print("CRITICAL events: {}".format(len(critical_events)), file=out)
    print("\n" + "=" * 37, file=out)
    print(f"{'UNIQUE ERROR MESSAGES':^36}", file=out)
    print("-" * 37, file=out)
    if unique_errors:
        for err in sorted(unique_errors):
            print(f"- {err}", file=out)
    else:
        print("(none)", file=out)

    print("\n" + "=" * 37, file=out)
    print(f"{'UNIQUE CRITICAL MESSAGES':^36}", file=out)
    print("-" * 37, file=out)
    if critical_events:
        for c in sorted(critical_events):
            print(f"- {c}", file=out)
    else:
        print("(none)", file=out)


