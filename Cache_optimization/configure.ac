# Initialize autoconf
AC_INIT([Assignment4], [1.0])
AM_INIT_AUTOMAKE([foreign])

# Check for C and C++ compilers
AM_PATH_CPPUNIT(1.9.6)
AC_PROG_CC
AC_PROG_CXX
AC_PROG_RANLIB
AC_PROG_INSTALL

# Check for C++11 support and add the appropriate flag
AX_CXX_COMPILE_STDCXX_11(noext, mandatory)

# Configure Makefiles
AC_CONFIG_FILES([Makefile
		 src/utilities/Makefile
                 src/exec/Makefile
		 src/tests/Makefile])
AC_OUTPUT
