from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import subprocess
import os
from os.path import join, exists
import shutil
import sys
from pathlib import Path

        
with open('requirements.txt') as f:
    required = f.read().splitlines()
    
setup(
    name="psl_toolchain",
    packages=["psl_toolchain", "psl_toolchain.packages"],
    #scripts=["bin/SwiftPackageWriter",],
    entry_points={
        "console_scripts": ["psl_toolchain=psl_toolchain.toolchain:main"]
    },
    install_requires=required
)
