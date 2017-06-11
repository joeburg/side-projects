#ifndef macros_hpp
#define macros_hpp

#include <sstream>
#include <stdexcept>

/* Macros to throw exceptions */

#define ThrowException(msg) \
{std::stringstream s; s << __FILE__ << ":" << __LINE__ << ":" << __func__ << ": " << msg; \
throw std::runtime_error(s.str());}

#define CloseFileThrowException(f,msg) \
{fclose(f); std::stringstream s; s << __FILE__ << ":" << __LINE__ << ":" << __func__ << ": " << msg; \
throw std::runtime_error(s.str());}

#endif /* macros_hpp */
