import subprocess
import sys
import tempfile
import time
from pathlib import Path

from rich import print


class RunResult:
    def __init__(self, stdout: str, stderr: str, returncode: int):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode


def run(code: str, silent: bool = False, debug: bool = False) -> RunResult:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        source = tmpdir / "out.S"
        executable = tmpdir / "out.elf"

        source.write_text(code)

        start_compile = time.perf_counter()
        subprocess.run(
            [
                "riscv64-unknown-elf-gcc",
                "-march=rv32im",
                "-mabi=ilp32",
                "-nostdlib",
                "-Wl,--no-relax",
                "-o",
                executable,
                source,
            ],
            check=True,
            stderr=subprocess.DEVNULL if "-v" not in sys.argv else None,
        )

        if debug:
            print(
                f"[cyan]Compiled in {(time.perf_counter() - start_compile) * 1000:.2f} ms[/]"
            )

            debug_dir = Path("../debug")
            debug_dir.mkdir(exist_ok=True)
            debug_executable = debug_dir / "out.elf"
            with open(debug_executable, "wb") as f:
                f.write(executable.read_bytes())

        start_run = time.perf_counter()
        output = subprocess.run(
            ["qemu-riscv32", executable], check=False, capture_output=True, text=True
        )
        if debug:
            print(f"[cyan]Ran in {(time.perf_counter() - start_run) * 1000:.2f} ms[/]")

        if not silent:
            print(output.stdout)

            print(
                f"\n[{'green' if output.returncode == 0 else 'red'}]Program exited with code {output.returncode}[/]"
            )

        return RunResult(
            stdout=output.stdout, stderr=output.stderr, returncode=output.returncode
        )
