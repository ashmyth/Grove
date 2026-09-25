"""
Grove (GeoPrithvi-Agri) Unified Single-Command Runner
Launches the entire full-stack application (FastAPI + Embedded React Frontend) in one shot.
"""

import sys
import subprocess
import webbrowser
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = ROOT_DIR / "frontend"
DIST_DIR = FRONTEND_DIR / "dist"

def main():
    print("=" * 65)
    print("  🌿 GROVE (GeoPrithvi-Agri) — Unified Full-Stack Application")
    print("=" * 65)

    # 1. Verify frontend build exists, or build it if missing
    if not (DIST_DIR / "index.html").exists():
        print("\n[1/3] Building React frontend production bundle...")
        build_res = subprocess.run(["npm", "run", "build"], cwd=str(FRONTEND_DIR), shell=True)
        if build_res.returncode != 0:
            print("ERROR: Failed to build React frontend.")
            sys.exit(1)
    else:
        print("\n[1/3] React frontend production bundle verified at frontend/dist/.")

    # 2. Check uvicorn availability
    try:
        import uvicorn
    except ImportError:
        print("ERROR: uvicorn is not installed. Run: pip install -r backend/requirements.txt")
        sys.exit(1)

    # 3. Ensure port 8000 is free (prevent WinError 10048 address in use)
    import socket
    port = 8000
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        is_port_in_use = (s.connect_ex(("127.0.0.1", port)) == 0)
    
    if is_port_in_use:
        print(f"Notice: Port {port} is occupied. Releasing port...")
        try:
            cmd = f"netstat -ano | findstr :{port}"
            output = subprocess.check_output(cmd, shell=True).decode("utf-8", errors="ignore")
            pids = set()
            for line in output.strip().splitlines():
                parts = line.split()
                if len(parts) >= 5 and "LISTENING" in parts:
                    pids.add(parts[-1])
            for pid in pids:
                if pid and pid != "0":
                    subprocess.run(f"taskkill /PID {pid} /F", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(1.0)
        except Exception as e:
            print(f"Warning: Could not auto-clear port: {e}")

    # 4. Schedule auto-opening the browser
    target_url = f"http://127.0.0.1:{port}/"
    print(f"\n[2/3] Launching unified FastAPI server on {target_url}...")
    
    def open_browser():
        time.sleep(1.2)
        print(f"\n[3/3] Opening {target_url} in your default browser...")
        webbrowser.open(target_url)

    import threading
    threading.Thread(target=open_browser, daemon=True).start()

    # 4. Start single-process FastAPI app serving both API and React frontend
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=False)

if __name__ == "__main__":
    main()
