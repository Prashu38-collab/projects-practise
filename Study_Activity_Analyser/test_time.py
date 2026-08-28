from datetime import datetime


def calculate_duration(start_time, end_time):
    return end_time - start_time


start = datetime(2026, 8, 28, 10, 15, 0)
end = datetime(2026, 8, 28, 11, 45, 0)

duration = calculate_duration(start, end)

print("Duration:", duration)
print("Seconds:", duration.total_seconds())