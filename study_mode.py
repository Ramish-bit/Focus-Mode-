import os, sys, time, subprocess, webbrowser, platform
import psutil

BLOCK_SITES = ["youtube.com", "reddit.com", "instagram.com", "twitter.com", "9gag.com"]
KILL_APPS   = ["Discord", "Spotify", "Steam", "Telegram"]
HOSTS_PATH  = "/etc/hosts" if platform.system() != "Windows" else r"C:\Windows\System32\drivers\etc\hosts"
REDIRECT    = "127.0.0.1"
LMS_URL     = "https://your-college-portal.edu"   # <-- change this
VSCODE_CMD  = "code"                               # <-- adjust if needed

def kill_distractions():
    killed = 0
    for proc in psutil.process_iter(["name", "pid"]):
        for app in KILL_APPS:
            if app.lower() in proc.info["name"].lower():
                try:
                    proc.kill()
                    print(f"  [✓] Killed {proc.info['name']} (PID {proc.info['pid']})")
                    killed += 1
                except psutil.NoSuchProcess:
                    pass
    if killed == 0:
        print("  [·] No distracting apps were running")

def block_sites():
    try:
        with open(HOSTS_PATH, "r+") as f:
            content = f.read()
            f.seek(0, 2)
            f.write("\n# --- STUDY BLOCK START ---\n")
            for site in BLOCK_SITES:
                if site not in content:
                    f.write(f"{REDIRECT} {site}\n")
                    f.write(f"{REDIRECT} www.{site}\n")
            f.write("# --- STUDY BLOCK END ---\n")
        print(f"  [✓] Blocked {len(BLOCK_SITES)} distracting sites")
    except PermissionError:
        print("  [!] Permission denied — run with sudo to block sites")

def unblock_sites():
    try:
        with open(HOSTS_PATH, "r") as f:
            lines = f.readlines()
        with open(HOSTS_PATH, "w") as f:
            skip = False
            for line in lines:
                if "# --- STUDY BLOCK START ---" in line:
                    skip = True
                if not skip:
                    f.write(line)
                if "# --- STUDY BLOCK END ---" in line:
                    skip = False
        print("  [✓] All sites unblocked")
    except PermissionError:
        print("  [!] Permission denied — run with sudo to unblock sites")

def open_workspace():
    try:
        subprocess.Popen([VSCODE_CMD])
        print("  [✓] Launched VS Code")
    except FileNotFoundError:
        print("  [!] VS Code not found — check VSCODE_CMD path")
    time.sleep(1.5)
    webbrowser.open(LMS_URL)
    print("  [✓] Opened college portal in browser")

def countdown(minutes):
    total = minutes * 60
    try:
        for remaining in range(total, -1, -1):
            m, s = divmod(remaining, 60)
            print(f"\r  ⏳ {m:02d}:{s:02d} remaining  ", end="", flush=True)
            time.sleep(1)
        print("\n  [✓] Session complete! Great work. 🎉")
    except KeyboardInterrupt:
        print("\n  [!] Timer interrupted")
        raise

def study_mode(duration=25):
    print(f"\n{'='*45}")
    print(f"   🎯 STUDY MODE — {duration} minute session")
    print(f"{'='*45}\n")

    kill_distractions()
    block_sites()
    open_workspace()

    print(f"\n  [✓] Setup complete. Starting {duration}-min timer...\n")

    try:
        countdown(duration)
    except KeyboardInterrupt:
        print("  [!] Session ended early")
    finally:
        print("\n  Reverting changes...")
        unblock_sites()
        print(f"\n{'='*45}")
        print("   SESSION ENDED — Nice work!")
        print(f"{'='*45}\n")

if __name__ == "__main__":
    duration = int(sys.argv[1]) if len(sys.argv) > 1 else 25
    study_mode(duration)
