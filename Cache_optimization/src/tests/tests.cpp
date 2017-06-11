//
//  tests.cpp
//  
//
//  Created by Joe Burg on 2/9/15.
//
//

#include <cppunit/ui/text/TestRunner.h>
#include <cppunit/TestCase.h>
#include <cppunit/TestCaller.h>
#include <cppunit/extensions/HelperMacros.h>
#include <memory>

#include "utilities.hpp"

class TransposeTest: public CppUnit::TestCase
{
    /* setup a suite of tests */
    CPPUNIT_TEST_SUITE( TransposeTest );
    CPPUNIT_TEST( TestTransposeSame );
    CPPUNIT_TEST_SUITE_END();
    
    public:
    TransposeTest() : CppUnit::TestCase("Transpose Test") {}
    
    /* implementation of the tests */
    void TestTransposeSame()
    {
        // intiialze matrix, transpose both ways and compare each index
        int size = 4096;
        int ldim = 4096;
        int blocksize = 256;
        
        double *a1 = new double[ldim*size];
        initmatrix(a1,size,ldim);
        int val1 = SimpleTranspose(a1,size,ldim);
        
        double *a2 = new double[ldim*size];
        initmatrix(a2,size,ldim);
        int val2 = OptimizedTranspose(a2,size,ldim,blocksize);
        
        bool same = true;
        for (int i=0; i < size; i++)
        {
            for (int j=i+1; j < ldim ; j++)
            {
                if (a1[j+i*ldim] != a2[j+i*ldim])
                {
                    same = false;
                    break;
                }
                else if (a1[i+j*ldim] != a2[i+j*ldim])
                {
                    same = false;
                    break;
                }
            }
        }
        CPPUNIT_ASSERT(same == true);
        CPPUNIT_ASSERT(val1 == 0);
        CPPUNIT_ASSERT(val2 == 0);
        delete[] a1; delete[] a2;
    }
};


int main(void)
{
    CppUnit::TextUi::TestRunner runner;
    runner.addTest(TransposeTest::suite());
    bool successful = runner.run();
    return !successful;
}
