Some libraries, including Intel MKL, will generate spurious Valgrind warnings.
After it has been confirmed that a given warning is spurious, it can be placed
in a suppressions file.  Running Valgrind with a suppressions file will exclude
these spurious warnings and let you focus on making sure there are no issues
with your own code.  A suppressions file has already been created for this
assignment and can be used using this syntax:

$ valgrind --suppressions=cme212.supp src/main data/references data/samples
