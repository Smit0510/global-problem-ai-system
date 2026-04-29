
import subprocess
import sys
import time
import socket
import webbrowser

# ------------------------------
# Utility functions
# ------------------------------

def run_step(name, command):
    print("\n" + "="*70)
    print(f"🚀 RUNNING: {name}")
    print("="*70)
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"❌ ERROR during step: {name}")
        sys.exit(1)
    print(f"✅ Completed: {name}")


def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


def start_ollama():
    print("\nChecking Ollama server...")
    if is_port_open(11434):
        print("✅ Ollama already running")
        return

    print("Starting Ollama server...")
    subprocess.Popen("ollama serve", shell=True)
    
    for _ in range(10):
        if is_port_open(11434):
            print("✅ Ollama started successfully")
            return
        time.sleep(1)

    print("⚠️ Could not confirm Ollama start. Please run 'ollama serve' manually.")


def open_dashboard():
    print("\nOpening dashboard...")
    url = "http://localhost:8501"
    time.sleep(3)
    webbrowser.open(url)


# ------------------------------
# Main Pipeline
# ------------------------------

def main():

    print("\n🌍 GLOBAL PROBLEM DISCOVERY AI PIPELINE")
    print("="*70)

    # Start Ollama
    start_ollama()

    # Data collection
    run_step(
        "Fetching Hacker News discussions",
        "python src/hn_scraper.py"
    )

    # Preprocessing
    run_step(
        "Cleaning and preprocessing text",
        "python src/preprocessing.py"
    )

    # Embeddings
    run_step(
        "Generating embeddings",
        "python src/create_embeddings.py"
    )

    # Clustering
    run_step("Clustering discussions into problems", "python src/cluster_discussions.py")
    print("\n📊 Launching Streamlit dashboard...")

    # Open dashboard in browser
    open_dashboard()

    subprocess.run(
        "python -m streamlit run src/dashboard.py",
        shell=True
    )


if __name__ == "__main__":
    main()
