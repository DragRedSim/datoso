"""List all installed seeds."""
from pydoc import locate
from datoso import __app_name__

def get_seed(seed, module):
    if module:
        return locate(f'{__app_name__}_seed_{seed}.{module}')
    return locate(f'{__app_name__}_seed_{seed}')

def installed_seeds():
    import importlib
    import pkgutil

    return {
        name: importlib.import_module(name)
        for finder, name, ispkg
        in pkgutil.iter_modules()
        if name.startswith(f'{__app_name__}_seed_')
    }


def seed_description(seed):
    seed = locate(f'{__app_name__}_seed_{seed}')
    return seed.__description__
