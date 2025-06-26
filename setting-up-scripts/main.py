#!/usr/bin/env python3
import os
from pathlib import Path

from renode_run import get_default_renode_path
from renode_run.utils import RenodeVariant
renode_bin = get_default_renode_path(variant=RenodeVariant.DOTNET_PORTABLE)

# Export only PYRENODE_BIN
os.environ["PYRENODE_BIN"]     = renode_bin
os.environ["PYRENODE_RUNTIME"] = "coreclr"

from pyrenode3.wrappers import Emulation, Monitor, TerminalTester
from Antmicro.Renode.Peripherals.UART import UARTBackend
from Antmicro.Renode.Analyzers import LoggingUartAnalyzer
from System import String

def run_emulation():
    # 1) Start Renode emulation
    emu = Emulation()
    mon = Monitor()
    emu.BackendManager.SetPreferredAnalyzer(UARTBackend, LoggingUartAnalyzer)

    # 2) Execute your existing script.resc
    resc = Path(__file__).parent / "script.resc"
    mon.execute_script(str(resc))

    # 3) Wait for the “Hello World! bt610” UART message
    machine = emu.get_mach("bt610")
    if machine is None:
        raise RuntimeError("Machine 'bt610' not found in the emulation.")
    else:
        print(f"Found machine")
    tester  = TerminalTester(machine.sysbus.uart0, timeout=5)
    tester.WaitFor(String("Hello World! bt610"), pauseEmulation=True)
    print("Received expected UART message.")
    # 4) Tear down emulation
    emu.Dispose()
    
    #read the log file
    log = Path("hello_world-renode.log")
    if log.exists():
        with log.open("r") as f:
            print(f.read())
    else:
        print("Log file not found.")
if __name__ == "__main__":
    run_emulation()
