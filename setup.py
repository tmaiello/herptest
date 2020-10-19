from setuptools import setup

setup(
    name='herptest',
    version='0.9.9.3',
    packages=['herptest',],
    url='https://github.com/cacticouncil/herptest',
    license='GPL 3',
    author='Jeremiah Blanchard',
    author_email='jjb@eng.ufl.edu',
    description='Test suite tools for instructors',

    install_requires=[
        'paramiko',
        'vix',
        'virtualbox',
        'pyside2'
    ],
    package_data={'herptest': ['herptest/*.png']},
    include_package_data=True,

    entry_points =
    { 'console_scripts':
        [
            'elma = herptest.extract_lms_archive:main',
            'herp = herptest.run_test_suite:main',
            'peng-gui = herptest.gui:main'
        ]
    }
)
