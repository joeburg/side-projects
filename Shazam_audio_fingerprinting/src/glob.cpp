#include <glob.h>

#include <string>
#include <vector>

#include "glob.hpp"

/* C++ glob.glob style function. 
Reference: http://stackoverflow.com/questions/8401777/simple-glob-in-c-on-unix-system */

std::vector<std::string> glob(std::string path)
{
  glob_t glob_result;
  glob(path.c_str(), GLOB_TILDE, NULL, &glob_result);

  std::vector<std::string> filelist;
  for (unsigned int i = 0; i < glob_result.gl_pathc; i++)
    filelist.push_back(std::string(glob_result.gl_pathv[i]));

  globfree(&glob_result);
  return filelist;
}
