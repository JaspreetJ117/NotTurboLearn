import os
import subprocess
import random
from datetime import datetime, timedelta

# --- INPUT ---
start_date_str = input("Enter start date (YYYY-MM-DD): ").strip()
end_date_str = input("Enter end date (YYYY-MM-DD): ").strip()

start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

if end_date < start_date:
    raise ValueError("End date must be after start date!")

# File we will edit
readme_file = "README.md"
if not os.path.exists(readme_file):
    with open(readme_file, "w") as f:
        f.write("# Project\n\n")

commit_count = 0
day_count = 0

current_date = end_date

while current_date.date() >= start_date.date():
    day_count += 1

    # 65% chance of committing this day
    if random.random() < 0.65:
        num_commits = random.randint(1, 50)

        for i in range(num_commits):
            # Append to README.md
            with open(readme_file, "a") as f:
                f.write(f"\nCommit {i+1} on {current_date.strftime('%Y-%m-%d')}\n")

            subprocess.run(["git", "add", readme_file], check=True)

            # Random time between 9 AM and 9 PM
            random_hour = random.randint(9, 21)
            random_minute = random.randint(0, 59)
            random_second = random.randint(0, 59)
            commit_time = current_date.replace(
                hour=random_hour,
                minute=random_minute,
                second=random_second
            )

            # Timezone offset (auto-detect system local offset)
            local_offset = datetime.now().astimezone().strftime("%z")
            commit_date = commit_time.strftime(f"%Y-%m-%d %H:%M:%S {local_offset}")

            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"] = commit_date
            env["GIT_COMMITTER_DATE"] = commit_date

            subprocess.run(
                ["git", "commit", "-m", f"Backdated commit {i+1} for {current_date.strftime('%Y-%m-%d')}"],
                check=True,
                env=env,
            )
            commit_count += 1
    else:
        print(f"⏭️ Skipping {current_date.strftime('%Y-%m-%d')} (no commits)")

    current_date -= timedelta(days=1)

print(f"\n✅ Done! Created {commit_count} commits across {day_count} days between "
      f"{start_date.strftime('%Y-%m-%d')} and {end_date.strftime('%Y-%m-%d')} (with skipped days).")
