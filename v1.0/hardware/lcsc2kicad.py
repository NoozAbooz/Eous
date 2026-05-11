import argparse
import os
import shutil
import subprocess
import sys

def run_easyeda2kicad_from_file(input_file, output_dir, python_exec=None):
    # Fix 1: Default to the current Python interpreter if none provided
    if python_exec is None:
        python_exec = sys.executable

    input_file = os.path.abspath(os.path.expanduser(input_file))
    output_dir = os.path.abspath(os.path.expanduser(output_dir))

    if not os.path.isfile(input_file):
        print(f"Error: File not found: {input_file}")
        return 2

    # Verify executable exists
    found = shutil.which(python_exec) or os.path.exists(python_exec)
    if not found:
        print(f"Warning: Python executable '{python_exec}' not found. Attempting to proceed anyway.")

    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, "r", encoding="utf-8") as f:
        # .strip() handles both \n (Linux) and \r\n (Windows) endings
        lines = [line.strip() for line in f if line.strip() and not line.lstrip().startswith("#")]

    if not lines:
        print("No LCSC IDs found in input file.")
        return 0

    for idx, lcsc_id in enumerate(lines, start=1):
        cmd = [
            python_exec,
            "-m", "easyeda2kicad",
            "--full",
            f"--lcsc_id={lcsc_id}",
            f"--output={output_dir}",
            f"--project-relative",
            f"--overwrite",
        ]
        
        print(f"[{idx}/{len(lines)}] Running: {' '.join(cmd)}")
        
        try:
            # Fix 2: shell=True is often required on Windows to resolve the PATH correctly
            # Fix 3: Use a string for the command when shell=True for better Windows reliability
            subprocess.run(" ".join(cmd) if os.name == 'nt' else cmd, check=True, shell=(os.name == 'nt'))
        except subprocess.CalledProcessError as e:
            print(f"❌ Error processing {lcsc_id}: {e}")
        except FileNotFoundError as e:
            print(f"❌ Executable not found: {e}")
            return 3

    print("✅ All commands completed.")
    return 0

def main(argv=None):
    parser = argparse.ArgumentParser(description="Run easyeda2kicad for a list of LCSC IDs.")
    parser.add_argument("input_file", nargs="?", default="./lcsc.txt", help="Path to file with one LCSC ID per line")
    parser.add_argument("output_dir", nargs="?", default="./lib/lcsc", help="Output directory")
    parser.add_argument("--python", dest="python_exec", default=None,
                        help="Python executable to use (default: current interpreter)")
    args = parser.parse_args(argv)

    return_code = run_easyeda2kicad_from_file(args.input_file, args.output_dir, args.python_exec)
    sys.exit(return_code if isinstance(return_code, int) else 0)

if __name__ == "__main__":
    main()