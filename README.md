# HerpTest - The Python Instructional Test Suite System

```
Team Peng - CIS 4930 - Python Term Project
- Tyler Maiello
- Emma Andrews
- Matthew Baumaister
- Matthew McDermott
- Gerard Avecilla
```

This test suite it built to facilitate testing of student projects by teachers according to a predefined specification.

This package includes five primary tools:

- `herptest.toolbox`, which contains standardized / cross-platform function calls (currently only library loading)
- `elma`, a command line tool to extract student submissions: (E)xtract (LM)S (A)rchive. Support is limited to Canvas. 
- `herp`, a command line tool to run a project test suite as specified by the user.
- `peng-gui`, a graphical interface built on top of the other command-line tools in this package.
- `csv-upload`, a CLI tool to automatically push a well formatted CSV of student grades and comments to a specified assignment.


## HerpTest Toolbox (`herptest.toolbox`)

The toolbox includes the following helper functions, intended to be cross-platform:

`loadTempLibrary(directory, name)`
Returns library loaded with temporary filename; this is necessary on some systems to avoid name collisions.

`loadLibrary(directory, name)`
Returned regularly loaded library

`unloadLibrary(library)`
Unloads the library passed as a parameter

`findLibrary(directory, name)`
Attempts to find any valid version of the library, name-wise (lib, so, etc)

`loadModule(filename)`
Loads a Python module from the supplied filename and returns it.


## Extracting LMS Archives (`elma`)
The 'elma' tool will extract a mass-download archive file from LMS systems (such as Canvas) to a submissions directory,
accounting for common renaming schemes and potential student name collisions.

usage: `elma [-h] FILENAME DESTINATION`


## Running Unit Test Suite (`herp`)

The `herp` command will begin the running of unit tests of all target project. It can take the following arguments:

usage: `herp [-h] [-V] [-q] [-d] [suite_path] [target_path]`

positional arguments:
  suite_path     path of test suite to load (default: ./)
  target_path    path of the target projects to consider (by subdirectory / folder) (default: Projects)

optional arguments:

  `-h`, `--help`     show this help message and exit
  
  `-V`, `--version`  show program's version number and exit
  
  `-q`, `--quiet`    execute in quiet mode (default: False)
  
  `-d`, `--debug`    display debug information (default: False)

(currently limited to library loading / execution)


Upon startup, the herp utility will optionally initialize the framework specified in the settings. This framework is
only built and initialized once for all students; any items that must be rebuilt for each student should be handled on
an per-subject (student) basis. The herp utility provides a mechanism to initialize and clean up at the framework,
subject, and project level (where there is one framework used to test many subjects, and each subject has one or more
projects that are tested individually.)

The test suite is identified by a "config.py" file that is loaded as a module. The config file must provide the
following interface to the testing system:

`--project` submodule object (config.project)

`--build` namespace object (config.build)

These objects are further described below.

### Project Submodule
The project submodule should provide the following interface to the testing system:

### Variables
`projectPenalties`
List of ordered pairs representing overall project test penalties (such as for execution time). Overall penalties are
tested for only once for an entire project, rather than for each individual data test case. List is formatted as:
`[ ( str:"PenaltyName", float:MAX_PENALTY )* ]`

If `projectPenalties` is empty or "None", this has no effect. (Note that the project penalties listed must be supported
by the testing functions below.)

`testCasePenalties`
List of ordered pairs representing penalties applied to individual test cases. These are tested for each data test
case. List is formatted as:
`[ ( str:"PenaltyName", float:MAX_PENALTY )* ]`

If `testCasePenalties` is empty or "None", this has no effect. (Note that the case test penalties listed must be
supported by the testing functions below.)

`maxPenalty`
This value identifies the maximum fraction of the grade that can be reduced due to penalties overall. 0.0 would mean
no penalties will be assessed, while 1.0 would mean students could lose all credit potentially.

`projects`
A list of projects to be tested for each subject (student). Project list is in the following format:
`[ ( str:"display name", str:"internal name", float:POINT_VALUE )+ ]`

The display name is used in output about project testing, while the internal name is passed to the `initializeProject`
function outlined below. The point value identifies how the project should be scored.

### Functions

#### Initialization / Shutdown of Test Suite
`initializeFramework(framework_bin)`
This function is called after building the framework. It is passed the framework output (binary) directory. It should
return any framework_context that is important to properly shutdown / cleanup the framework.

`shutdownFramework(framework_context)`
This function will be called when all testing is done in order to shutdown / clean up the framework. The context passed
in is identical to that returned by the initializeFramework function.

`initializeSubject(subject_bin)`
This function is called after the subject project(s) are built but before they are tested. It is passed the subject
output (binary) directory. It should return any subject_context that is important to properly shutdown / cleanup once
all of the subject's project tests have been completed.

`shutdownSubject(subject_context)`
This function will be called when all testing is done for this subject. The subject_context passed in is identical to
that returned by the initializeSubject function.

`initializeProject(identifier, framework_context, subject_context, config.project)`
This function is called by the test suite to prepare a project to be tested. It includes the project's internal string
identifier as well as the framwork / subject contexts (returned by the initializers) and the project settings. Is
should return any project_context that is important to properly shutdown / cleanup the project after testing is done.

`shutdownProject(project_context)`
This function will be called when all testing is done for this project. The project_context passed in is identical to
that returned by the initializeProject function.

#### Testing Functions
`getNumberOfTests(project_context)`
Returns the number of data test cases available for the project identified by project_context.

`getTestDescription(test_number, project_context)`
Returns a string describing the test identified by test_number and project_context.

`runCaseTest(test_number, project_context)`
Runs the test identified by test_number and project_context, returning a score.

`runCasePenalty(penalty_number, test_number, project_context)`
Runs the test identified by test_number and project_context, capturing the penalty identified by penalty_number.

`runProjectPenalty(penalty_number, project_context)`
Runs the penalty test identified by penalty_number and project_context, returning its value.

`analyzeRunLog(location)`
Analyzes the run.log returned from the VM, returning a string containing the values to add to the csv and the total score.

### Build Namespace
The build namespace objects holds paths and build commands. It must provide the following interface:

`base (string)`
Path to the base project source files; these will be copied into the target before the subject (student)
submission files are copied.

`destination (string)`
Path where student files should be copied. Usually inside the subject_src directory (see subject_src).

`resources (string)`
Path to resources used by the project (if any; may be **None**)

`subject_src (string)`
Path to source files for the target / subject project to be built. Usually contains the destination directory.

`subject_bin (string)`
Path in which the subject project will be built

`framework_src (string)`
Path to source files for the framework used for testing the projects

`framework_bin (string)`
Path in which the framework will be built

`prep_cmd (list of strings)`
Command to be used to prepare the build (e.g., autoconf or cmake). This is a list of strings consisting of the command
followed by its arguments.

`compile_cmd (list of strings)`
Command to be used to compile the build (e.g., make or devenv). This is a list of strings consisting of the command
followed by its arguments.


## Building & Running Graphical Interface (`peng-gui`)

To run the GUI from WSL2, VcXsrv should be running first.

Some additional OS packages may be required (especially on stock distributions of WSL2):

`sudo apt install libxkbcommon-x11-0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-render-util0 libxcb-xfixes0 libxcb-xinerama0`

Additionally, qtmake may require the following:

`wget https://download.qt.io/development_releases/prebuilt/libclang/libclang-release_60-linux-Rhel7.2-gcc5.3-x86_64-clazy.7z`
`7z x ./libclang-release_60-linux-Rhel7.2-gcc5.3-x86_64-clazy.7z`
`export LLVM_INSTALL_DIR=$PWD/libclang`

## Using The CSV Uploading Tool (csv-upload)

To run from CLI after building herp, run `csv-upload` with optional flags `--help`, `--version`, and `--setupenv`

Where `--setupenv` will run you through the installation process of importing your Canvas API Token.


## Building this Package

To build package:
`python3 setup.py sdist bdist_wheel`

To upload:
`python3 -m twine upload dist/*`

