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
    'long_description': "# agglomerative_partitioning\n\npartitioning Image by Features in Agglomeratively\n\n## KclassImage(k, feature, target, shape)\n\n- `k` is a number of classes\n- `feature` is a feature data\n- `target` is a class data\n- `shape` is a Image shape\n\nit saves `f'{k}.jpg'`\n\n## dist_table(feature, nrows, ncols)\n\n- `feature` is a feature data\n- `nrows` and `ncols` are Image shape\n\nit return Feature distance table but only between neighboring samples in Image cordinates.\n\n## agglomerative_clustering(feature, dist, K)\n\n- `feature` is a feature data\n- `dist` is a feature distance table made by `dist_table()`\n- `K` is a number of target classes\n\nit return target class data by samples\n\n# example\n\nFollowing code make 128 partitions in sample.jpg, reduce its colors and save to 128.jpg\n  \n```{python}\nfrom agglomerative_partitioning as ap\n\nImageFileName = 'sample.jpg'\nK = 128\n\nim = np.array(Image.open(ImageFileName))\nnrows = im.shape[0]\nncols = im.shape[1]\n\nfeature = im.reshape((nrows * ncols, -1))\n\ndist = ap.dist_table(feature, nrows, ncols)\n\ntarget = ap.agglomerative_clustering(feature, dist, K)\n\nap.KclassImage(K, feature, target, (nrows, ncols))\n```\n\n![sample.jpg] ![128.jpg]\n",
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
