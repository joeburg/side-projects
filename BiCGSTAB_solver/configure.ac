# Initialize autoconf
AC_INIT([Assignment3], [1.0])
AM_INIT_AUTOMAKE([foreign])

# Check for C and C++ compilers
AC_PROG_CC
AC_PROG_CXX

# Check for C++11 support and add the appropriate flag
AX_CXX_COMPILE_STDCXX_11(noext, mandatory)

# Configure Makefiles
AC_CONFIG_FILES([Makefile
                 src/Makefile])
AC_OUTPUT
