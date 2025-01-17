#! /bin/python3

import typer
import subprocess

from rich.console import Console
from rich.table import Table
from typers import samba, linbo, devices, users, up


console = Console()
app = typer.Typer()
app.add_typer(samba.app, name='samba')
app.add_typer(linbo.app, name='linbo')
app.add_typer(devices.app, name='devices')
app.add_typer(users.app, name='users')
app.add_typer(up.app, name='up')

@app.command(help="Lists linuxmuster.net packages installed.")
def version():
    packages = Table()
    packages.add_column("Status", style="green")
    packages.add_column("Packages", style="cyan")
    packages.add_column("Version", style="bright_magenta")

    command = "dpkg -l | grep 'linuxmuster\|sophomorix'"
    p = subprocess.Popen(command, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    for package in p.stdout.readlines():
        details = package.decode().split()
        status, name, version  = details[:3]
        packages.add_row(status, name, version)
    console.print(packages)

if __name__ == "__main__":
    app()
