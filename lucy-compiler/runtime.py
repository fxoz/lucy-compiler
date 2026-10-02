import sys
import subprocess
import tempfile
from pathlib import Path

from rich import print


def run(code: str):
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        source = tmpdir / "out.S"
        executable = tmpdir / "out.elf"

        source.write_text(code)

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

        result = subprocess.run(["qemu-riscv32", executable], check=False)

        print(
            f"\n[{'green' if result.returncode == 0 else 'red'}]Program exited with code {result.returncode}[/]"
        )
