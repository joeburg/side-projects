# Initialize autoconf
AC_INIT([Assignment5], [1.0])
AM_INIT_AUTOMAKE([foreign])

# Check for Intel C++ compiler
AC_PROG_CC(["icc -mkl"])
AC_PROG_CXX(["icc -mkl -std=c++11"])

# Check for libsndfile
AC_CHECK_HEADERS(sndfile.h, ,[AC_MSG_ERROR([Could not find header file for libsndfile])])
AC_CHECK_LIB(sndfile, sf_open, ,[AC_MSG_ERROR([Could not find library file for libsndfile])])

# Configure Makefiles
AC_CONFIG_FILES([Makefile
                 src/Makefile])
AC_OUTPUT
