#!/usr/bin/env python3
"""
Fork terminal tool
"""
import subprocess
import sys
import platform
import os


def fork_terminal(command: str) -> str:
    """
    Fork a terminal session to run a command.

    Args:
        command: The command to run in the forked terminal

    Returns:
        str: Status message
    """
    system = platform.system()
    cwd = os.getcwd()

    try:
        if system == "Darwin":  # macOS
            # Use osascript to open new Terminal window in the current directory
            # Escape double quotes in command and cwd for AppleScript
            escaped_command = command.replace('"', '\\"')
            escaped_cwd = cwd.replace('"', '\\"')
            applescript = f'''
            tell application "Terminal"
                do script "cd \\"{escaped_cwd}\\" && {escaped_command}"
                activate
            end tell
            '''
            process = subprocess.Popen(
                ["osascript", "-e", applescript],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            process.wait()
            return f"Forked macOS Terminal in {cwd} with command: {command}"

        elif system == "Linux":
            # Prepend cd command to ensure correct working directory
            full_command = f'cd "{cwd}" && {command}'

            # Try common Linux terminal emulators with working directory support
            terminals = [
                ("gnome-terminal", ["--working-directory", cwd, "--", "bash", "-c", command]),
                ("xterm", ["-e", f'bash -c "cd \\"{cwd}\\" && {command}"']),
                ("konsole", ["--workdir", cwd, "-e", command])
            ]

            for term, args in terminals:
                try:
                    subprocess.Popen([term] + args)
                    return f"Forked {term} in {cwd} with command: {command}"
                except FileNotFoundError:
                    continue

            # Fallback to background process with correct working directory
            process = subprocess.Popen(
                full_command,
                shell=True,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return f"Running in background (PID {process.pid}) in {cwd}: {command}"

        else:
            return f"Unsupported platform: {system}"

    except Exception as e:
        return f"Error: {str(e)}"


def main():
    if len(sys.argv) < 2:
        print("Usage: fork_terminal.py <command>")
        print("Example: fork_terminal.py 'echo Hello World'")
        sys.exit(1)

    command = " ".join(sys.argv[1:])
    result = fork_terminal(command)
    print(result)


if __name__ == "__main__":
    main()
