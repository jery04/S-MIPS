# S‑MIPS — Computer Architecture 🧠💻⚙️

Technical template for a small educational MIPS-like CPU. This repository provides:
- an assembler to convert `.asm` files into Logisim memory banks 📄➡️💾
- an automatic test runner that executes assembled tests in Logisim 🧪
- a price calculator to estimate the "cost" of a Logisim circuit (used for grading) 💰

Use this README to understand repository layout, how to build tests, run them, and how the evaluation tools work. 🚀

**Quick links**
- Template circuit: `s-mips-template.circ`
- Example implementation: `s-mips.circ`
- Tests directory: `tests/` (contains many `.asm` testcases)
- Output folder for test runner: `tests-out/`

**Requirements** 🛠️
- Python 3 (Unix: `python3`; Windows: `python`) 🐍
- Logisim CLI available as `logisim` in PATH 🔌
- Unix-like shell recommended for the provided scripts, but Windows PowerShell can be used with minor adjustments 🪟

**Repository Structure (root)** 📁
- `assembler.py`: Assembler that converts a single `.asm` file into memory bank files (`Bank`, `Bank0`, `Bank1`, `Bank2`, `Bank3`). Usage: `python3 assembler.py infile.asm -o output_dir` 🧩
- `test.py`: Test runner that scans a tests directory, assembles each `.asm` test, and runs them in Logisim. Usage example below. 🧪
- `price.py`: Price/complexity estimator for a Logisim `.circ` file. It inspects the circuit and computes a numeric "price" based on components used. Use to verify the implementation cost limit. 💰
- `s-mips-template.circ`: The template Logisim circuit used by the test runner. It contains the test harness and expected subcircuit names. ⚙️
- `s-mips.circ`: Example or student CPU implementation (the circuit you will edit for projects). 🧩
- `tests/`: Directory with many `.asm` files. Each file may include a special comment line `#prints <expected-output>` (expected TTY output) and optionally `#limit <max-cycles>` to enforce speed limits. 📂
- `tests-out/`: Default output folder where `test.py` writes assembled banks and per-test subfolders (created by the runner). 📂

**How the tests work** 🔁
1. The test runner walks the `tests/` folder recursively and finds `.asm` files. 🔎
2. For each `.asm`, it runs the assembler (`assembler.py`) to produce memory bank files under `./tests-out/<testname>/`. 🛠️
3. It invokes Logisim with the template circuit to load the generated `Bank` file and runs until the CPU halts. The runner captures the TTY output and compares it with the `#prints` line from the `.asm` file. ✅/❌
4. If a `#limit <n>` line exists, the test also checks the number of clock ticks does not exceed that limit (performance check). ⏱️

**Common commands** 🧾

Unix / macOS / Linux (recommended):
```bash
# assemble a single test
python3 assembler.py tests/hello.asm -o ./outdir

# run the full test suite (from repo root)
python3 test.py tests s-mips.circ -o ./tests-out -t s-mips-template.circ
```

Windows (PowerShell / CMD):
```powershell
# assemble a single test
python assembler.py tests\\hello.asm -o .\\outdir

# run the full test suite
python test.py tests s-mips.circ -o .\\tests-out -t s-mips-template.circ
```

Note: `test.py` currently calls the assembler via `python3 assembler.py ...`. On Windows, edit the `compile()` function in `test.py` or make sure `python3` points to your Python executable (or create an alias). 📝

**Assembler details** 🛠️
- The assembler produces four byte-bank files named `Bank0`, `Bank1`, `Bank2`, `Bank3` plus a combined `Bank` file. These are Logisim memory images in `v2.0 raw` format. The output directory structure expected by the test runner is `tests-out/<testname>/Bank*`. 💾
- Typical assembler usage: `python3 assembler.py infile.asm -o output_dir` (see `assembler.py -h` for options). 📜

**Price calculator** 💰
- Run `price.py` to compute the cost of your `s-mips.circ` (or another circuit). Example:
```bash
python3 price.py s-mips.circ "S-MIPS" -l 100
```
- The tool returns a JSON object (or writes to `-o` file) and exits with non-zero if the price exceeds the provided `-l` limit. The default acceptance price is usually `100` units for grading. ⚖️

**How to add new tests** ✍️
1. Create a new `<name>.asm` under `tests/` (or a subfolder). 🧾
2. Add a line `#prints expected_output` to specify the expected TTY output. Optionally add `#limit <cycles>` to define a cycle limit. ⌛
3. Run the full test suite or assemble and run manually in Logisim as shown above. 🧪

**Manual testing with Logisim (GUI)** 🖥️
1. Run `assembler.py` to produce `Bank*` files for your test. 🧩
2. Open `s-mips.circ` in Logisim. 📂
3. Inside the `RAM Dispatcher` (or RAM component), load the `Bank` file (Right click → Load Image) or load `Bank0..Bank3` if using manual bank mode. ⚙️
4. Toggle the clock; the CPU should start executing the program and emit TTY output. 🔁

Tips & gotchas ⚠️
- Ensure the Logisim version you use supports the command-line flags the test runner expects. The runner calls `logisim` with `-tty`, `-load`, and other options. 🔍
- If tests fail due to assembly commands on Windows, modify `test.py` `compile()` to call `python` instead of `python3`. 🪛
- Do not modify files outside the CPU component when implementing the CPU — autograders ignore changes outside the CPU subcircuit. 🛡️
