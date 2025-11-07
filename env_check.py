#!/usr/bin/env python3
import platform
import subprocess
import os
from datetime import datetime

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None

def check_jetbrains():
    paths = [
        "/Applications/PyCharm.app",
        "/Applications/IntelliJ IDEA.app",
        "/Applications/WebStorm.app"
    ]
    found = [os.path.basename(p) for p in paths if os.path.exists(p)]
    return ", ".join(found) if found else None

def check_tools():
    print("🔍 Checking your development environment...\n")
    checks = {
        "OS": platform.system(),
        "Python": run_cmd("python3 --version") or run_cmd("python --version"),
        "Node.js": run_cmd("node -v"),
        "Git": run_cmd("git --version"),
        "VS Code": run_cmd("code --version"),
        "JetBrains IDE": check_jetbrains()
    }
    return checks

def suggest_installation(os_type, missing):
    suggestions = {}
    if os_type == "Windows":
        base = {
            "Python": "winget install Python.Python.3",
            "Node.js": "winget install OpenJS.NodeJS",
            "Git": "winget install Git.Git",
            "VS Code": "winget install Microsoft.VisualStudioCode"
        }
    elif os_type == "Darwin":  # macOS
        base = {
            "Python": "brew install python",
            "Node.js": "brew install node",
            "Git": "brew install git",
            "VS Code": "brew install --cask visual-studio-code"
        }
    else:  # Linux
        base = {
            "Python": "sudo apt install python3 -y",
            "Node.js": "sudo apt install nodejs npm -y",
            "Git": "sudo apt install git -y",
            "VS Code": "sudo snap install code --classic"
        }

    for tool in missing:
        suggestions[tool] = base.get(tool, "Manual installation required.")
    return suggestions

def generate_report(results, suggestions):
    missing = [tool for tool, value in results.items() if not value]
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("environment_report.md", "w") as f:
        f.write(f"# 🧰 Environment Check Report\n")
        f.write(f"Generated on: {now}\n\n")
        f.write(f"## System Info\n**OS:** {results['OS']}\n\n")

        f.write("## Tool Status\n")
        for tool, status in results.items():
            if tool != "OS":
                f.write(f"- **{tool}:** {'✅ Installed' if status else '❌ Missing'}\n")

        if missing:
            f.write("\n## Missing Tools & Install Commands\n")
            for tool in missing:
                f.write(f"- **{tool}:** `{suggestions[tool]}`\n")
        else:
            f.write("\n🎉 All tools are installed! You're ready to code!\n")

    print("\n✅ 'environment_report.md' has been generated.\n")

def main():
    results = check_tools()
    os_type = results["OS"]
    missing = [tool for tool, value in results.items() if not value]
    suggestions = suggest_installation(os_type, missing)
    generate_report(results, suggestions)

if __name__ == "__main__":
    main()
