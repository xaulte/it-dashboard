# ── Application Metadata ──────────────────────────────────
APP_NAME = "SERVER LOG ANALYSIS REPORT"
VERSION = "0.1.0"
CREATOR_NAME = "Austin Windorski"
PROF_NAME = "Prof. Frank Mora"
COURSE_NAME = "COP1034C - Python for IT"

import re
import os
from datetime import date

def parse_line(line):
    m = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(\w+)\] (.*)$', line)
    if not m: return None
    return {'date': m.group(1), 'severity': m.group(2), 'message': m.group(3)}

def run_parser(log_path='server.log', out_path='log_summary.txt'):
    severity_counts = {}
    unique_errors = set()
    critical_events = set()
    log_entries = []

    try:
        with open(log_path, 'r') as f:
            for line in f:
                entry = parse_line(line.rstrip('\n'))
                if not entry: continue

                severity = entry['severity']
                message = entry['message']
                
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
                if severity == "ERROR": unique_errors.add(message)
                if severity == "CRITICAL": critical_events.add(message)
                log_entries.append(entry)
    except FileNotFoundError:
        return f"Error: {log_path} not found."

    total_lines = len(log_entries)
    error_rate = (severity_counts.get("ERROR", 0) / total_lines) * 100 if total_lines > 0 else 0.0

    # Write the report
    with open(out_path, 'w') as out:
        out.write("=" * 37 + "\n")
        out.write(f"{APP_NAME} v{VERSION}\n")
        out.write(f"{CREATOR_NAME} | {PROF_NAME}\n")
        out.write(f"{COURSE_NAME} | {date.today().isoformat()}\n")
        out.write("=" * 37 + "\n")
        
        for level in ["INFO", "WARNING", "ERROR", "CRITICAL"]:
            out.write(f"{level:<9}: {severity_counts.get(level, 0):>4}\n")
            
        out.write(f"\nError rate: {error_rate:.2f}%\n")
        out.write(f"Unique ERROR messages: {len(unique_errors)}\n")
        out.write(f"CRITICAL events: {len(critical_events)}\n")
        
        out.write("\n" + "=" * 37 + "\n")
        out.write(f"{'UNIQUE ERROR MESSAGES':^36}\n" + "-" * 37 + "\n")
        for err in sorted(unique_errors): out.write(f"- {err}\n")
            
        out.write("\n" + "=" * 37 + "\n")
        out.write(f"{'UNIQUE CRITICAL MESSAGES':^36}\n" + "-" * 37 + "\n")
        for c in sorted(critical_events): out.write(f"- {c}\n")

    return f"Success: Parsed {total_lines} lines."

if __name__ == "__main__":
    # Allows it to still be run standalone if needed
    print(run_parser())