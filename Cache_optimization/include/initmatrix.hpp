//
//  initmatrix.h
//  
//
//  Created by Joe Burg on 2/8/15.
//
//

#ifndef initmatrix_hpp
#define initmatrix_hpp

#define BOOST_DISABLE_ASSERTS
#include "boost/multi_array.hpp"

boost::multi_array<double,2> initmatrix(int size, int ldim);

#endif /* initmatrix_hpp */
