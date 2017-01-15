from setuptools import setup, find_packages
import os
import re
import ast

HTTP = re.compile('^https?://.+#egg=(.+)$')


class UniversalSetupError(Exception):
    pass


def parse_dependency_info() -> dict:
    """Reads dependency info from requirements.txt"""
    packages = []
    links = []
    try:
        with open('requirements.txt') as dependencies:
            for line in map(str.strip, dependencies):
                link = HTTP.match(line)
                if link:
                    packages.append(link.group(1))
                    links.append(line)
                else:
                    packages.append(line)
    except FileNotFoundError:
        print('Missing requirements.txt')

    return {'install_requires': packages, 'dependency_links': links}


def read_metadata() -> dict:
    """Finds the package to install and returns it's metadata."""
    for entry in os.scandir():
        if entry.is_dir():
            package_init = os.path.join(entry.name, '__init__.py')
            if os.path.isfile(package_init):
                break
    else:
        raise UniversalSetupError('No package found!')

    metadata = {'name': entry.name}
    meta_names = {'__version__': 'version',
                  '__author__': 'author',
                  '__email__': 'author_email',
                  '__license__': 'license'}

    with open(package_init) as init:
        code = init.read()

    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        msg = 'Bad syntax in package init: %s'
        raise UniversalSetupError(msg % repr(package_init)) from exc

    docstring = ast.get_docstring(tree)
    if docstring is not None:
        metadata['description'] = docstring.split('\n')[0].strip()
    else:
        print('Missing package docstring!')

    for node in ast.iter_child_nodes(tree):
        try:
            value = node.value
            name = node.targets[0].id
            if name in meta_names:
                meta_name = meta_names[name]
                if meta_name in metadata:
                    msg = 'Repeat metadata assignment on line %d for item %s.'
                    print(msg % (node.lineno, repr(name)))
                metadata[meta_name] = value.s
        except AttributeError:
            pass

    unused_names = []
    for name in meta_names:
        meta_name = meta_names[name]
        if meta_name not in metadata:
            unused_names.append(name)

    if unused_names:
        print('The following metadata is missing: %s' % ', '.join(unused_names))

    metadata['packages'] = find_packages()
    metadata.update(parse_dependency_info())
    return metadata

setup(**read_metadata())
