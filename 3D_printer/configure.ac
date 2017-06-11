# Initialize autoconf and automake
AC_INIT([Assignment2], [1.0])
AM_INIT_AUTOMAKE([foreign])

# Generate a configuration header
AC_CONFIG_HEADERS([config.h])

# Check for programs
AC_PROG_CXX
AC_PROG_RANLIB

# Check for C++11 support and add the appropriate flag
AX_CXX_COMPILE_STDCXX_11(noext, mandatory)

# Configure Makefiles
AC_CONFIG_FILES([Makefile
                 src/geometry/Makefile
		 src/exec/Makefile])
AC_OUTPUT