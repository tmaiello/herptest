from setuptools import setup

setup(
    name='herptest',
    version='0.9.9.4',
    packages=['herptest',],
    url='https://github.com/cacticouncil/herptest',
    license='GPL 3',
    author='Jeremiah Blanchard',
    author_email='jjb@eng.ufl.edu',
    description='Test suite tools for instructors',
    install_requires=[
        'numpy',
        'certifi',
        'chardet',
        'idna',
        'python-dotenv',
        'requests',
        'urllib3',
        'paramiko',
        'vix',
        'virtualbox',
        'pyside2',
        'canvasapi'
    ],
    package_data={'herptest': ['herptest/*.png']},
    include_package_data=True,

    entry_points =
    { 'console_scripts':
        [
            'elma = herptest.extract_lms_archive:main',
            'herp = herptest.run_test_suite:main',
            'peng-gui = herptest.gui:main',
            'csv-upload = herptest.grade_csv_uploader:main',
            'canvas-push = herptest.canvas:main'
        ]
    }
)
