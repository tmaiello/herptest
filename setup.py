from setuptools import setup

setup(
    name='pengtest',
    version='0.9.9.4',
    packages=['pengtest',],
    url='https://github.com/tmaiello/herptest',
    license='GPL 3',
    author='Emma Andrews, Gerard Avecilla, Matthew Baumeister, Tyler Maiello, Matt McDermott',
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
        'canvasapi',
        'mosspy'
    ],
    package_data={'pengtest': ['pengtest/*.png']},
    include_package_data=True,

    entry_points =
    { 'console_scripts':
        [
            'elma = pengtest.extract_lms_archive:main',
            'peng = pengtest.run_test_suite:main',
            'peng-gui = pengtest.gui:main',
            'csv-upload = pengtest.grade_csv_uploader:main',
            'canvas-push = pengtest.canvas:main',
            'moss = pengtest.run_moss:main'
        ]
    }
)
