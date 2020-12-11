# CppCheckDiff
Do you need to compare CppCheck results between two branches in your CI? CppCheckDiff does that for you! Stop adding new CppCheck violations to your code base without the need of cleaning all errors at once!

## How to run

Expect, that results of check in `main` / `master` branch are stored in `data/main.cppcheck.xml` and results of check of development branch are stored in `data/branch.cppcheck.xml`.

### Find new errors
To find new errors introduced in your branch run:

`python cppcheckdiff.py data/branch.cppcheck.xml data/main.cppcheck.xml new.cppcheck.xml`

### Find resolved errors
To find errors resolved in your branch run:

`python cppcheckdiff.py data/main.cppcheck.xml  data/branch.cppcheck.xml resolved.cppcheck.xml`
