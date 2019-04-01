"""
This is a kind of complicated model, but it's incredibly useful.
Say you find a papaer form a few years ago with code. It's not unreasonable that there might
be dependency clashes, python clashes, clashes galore. This approach downloads a model, runs it
in it's own venv and makes everyone happy.
"""

import os
from pathlib import Path
import shutil
import subprocess

import git

from ethicml.algorithms.inprocess.in_algorithm import InAlgorithm
from ethicml.algorithms.inprocess.interface import conventional_interface
from ethicml.common import ROOT_PATH


ROOT_DIR = ROOT_PATH.parent


class InstalledModel(InAlgorithm):
    """ the model that does the magic"""
    def __init__(self, name: str, url: str, module: str, file_name: str):
        self.repo_name = name
        self.module = module
        self.file_name = file_name
        self.url = url
        self.clone_directory()
        self.create_venv()
        super().__init__(executable=str(Path(".") / name / module / '.venv' / 'bin' / 'python'))

    @property
    def name(self) -> str:
        pass

    def clone_directory(self):
        """
        Clones the repo
        """
        directory = Path(".") / self.repo_name
        if not os.path.exists(directory):
            os.makedirs(directory)
            git.Git(directory).clone(self.url)

    def create_venv(self):
        """
        Creates a venv based on the repos Pipfile
        """
        environ = os.environ.copy()
        environ["PIPENV_IGNORE_VIRTUALENVS"] = "1"
        environ["PIPENV_VENV_IN_PROJECT"] = "true"
        environ["PIPENV_YES"] = "true"
        environ["PIPENV_PIPFILE"] = str(Path(".") / self.repo_name / self.module / 'Pipfile')

        venv_directory = Path(".") / self.repo_name / self.module / ".venv"

        if not os.path.exists(venv_directory):
            subprocess.check_call("pipenv install", env=environ, shell=True)

    def _run(self, train, test):
        return super().run(train, test, sub_process=True)  # set sub_process always to True

    def _script_command(self, train_paths, test_paths, pred_path):
        """
        Overridden from parent - see there
        """
        args = conventional_interface(train_paths, test_paths, pred_path)
        return [str(Path(".") / self.repo_name / self.module / self.file_name)] + args

    def remove(self):
        """
        Removes the directory that we created in clone_directory
        """
        directory = Path(".") / self.repo_name
        try:
            shutil.rmtree(directory)
        except OSError as excep:
            print("Error: %s - %s." % (excep.filename, excep.strerror))
