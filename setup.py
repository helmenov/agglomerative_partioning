# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['agglomerative_partitioning']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0.0,<10.0.0', 'numpy>=1.22.1,<2.0.0']

setup_kwargs = {
    'name': 'agglomerative-partitioning',
    'version': '0.1.1',
    'description': '',
    'long_description': 'None',
    'author': 'Kotaro SONODA',
    'author_email': 'kotaro1976@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
