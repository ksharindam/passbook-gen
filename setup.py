from setuptools import setup
import platform
from passbook_gen import __version__, AUTHOR_NAME, AUTHOR_EMAIL

def readme():
    with open('README.md') as f:
        return f.read()

if platform.system()=='Linux':
    data_files = [('share/applications', ['data/passbook-gen.desktop']),
                ('share/icons/hicolor/scalable/apps', ['data/icons/passbook-gen.png'])]
else:
    data_files = []

setup(
    name='passbook-gen',
    version=__version__,
    description='Passbook Page Generator',
    long_description=readme(),
    long_description_content_type = 'text/markdown',
    keywords='price',
    url='http://github.com/ksharindam/passbook-gen',
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    license='GNU GPLv3',
    #install_requires=['PyQt5',],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: X11 Applications :: Qt',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3',
    ],
    packages=['passbook_gen'],
    entry_points={
      'gui_scripts': ['passbook_gen=passbook_gen.main:main'],
    },
    data_files = data_files,
    include_package_data=True,
    zip_safe=False
    )
