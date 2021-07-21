from setuptools import Command
from distutils.errors import DistutilsOptionError
from packaging.requirements import Requirement

class CondaEnv(Command):
    """
    Create and manipulate Conda environments from the package dependencies.
    """
    description = "create and update Conda dev environments"
    user_options = [
        ('python-version=', 'V', 'specify the environment Python version'),
        ('extras=', 'E', 'extras to activate'),
        ('save-env=', None, 'save environment to file'),
        ('create-env', None, 'create environment'),
        ('update-env', None, 'update environment'),
    ]
    boolean_options = [
        'create-env', 'update-env'
    ]

    def initialize_options(self):
        self.name = 'dev-env'
        self.channels = ['default']
        self.python_version = None
        self.extras = []

        self.save_env = None
        self.create_env = False
        self.update_env = False

        if sum(bool(x) for x in [self.save_env, self.create_env, self.update_env]) > 1:
            raise DistutilsOptionError('at most of --save-env, --create-env, --upate-env may be specified')

    def finalize_options(self):
        self.ensure_string_list('extras')
        self.ensure_string_list('channels')

    def run(self):
        deps = []
        pip_deps = []
        spec = {
            'name': self.name,
            'channels': [c for c in self.channels if c],
            'dependencies': deps,
        }
