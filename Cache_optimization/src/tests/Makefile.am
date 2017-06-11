# Rules for the test code (use `make check` to execute)
AM_CPPFLAGS = -I../../include
TESTS = tests
check_PROGRAMS = $(TESTS)
tests_SOURCES = tests.cpp
tests_CXXFLAGS = $(CPPUNIT_CFLAGS)
tests_LDADD = ../utilities/libutilities.a $(CPPUNIT_LIBS)