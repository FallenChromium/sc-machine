#include <iostream>
#include <fstream>

#include <boost/filesystem.hpp>
#include <boost/config.hpp>
#include <boost/program_options/detail/config_file.hpp>
#include <boost/program_options/parsers.hpp>

namespace pod = boost::program_options::detail;
namespace fs = boost::filesystem;

std::map<std::string, std::string> parse_config(std::string conf)
{
  fs::path conf_directory(conf);
  conf_directory = conf_directory.parent_path();

  std::ifstream config(conf);
  if (!config)
  {
    std::cerr << "File " << conf << " doesn't exist" << std::endl;
    return std::map<std::string, std::string>();
  }

  std::set<std::string> options;
  options.insert("*");
  std::map<std::string, std::string> result;

  try
  {
    for (pod::config_file_iterator i(config, options), e; i != e; ++i)
    {
      if (i->string_key == "Repo.Path")
        result.insert({"path", (conf_directory / i->value[0]).string()});
      if (i->string_key == "Extensions.Directory")
        result.insert({"ext", (conf_directory / i->value[0]).string()});
    }
  }
  catch (std::exception & e)
  {
    std::cerr << "Exception: " << e.what() << std::endl;
  }
  for (auto it : result)
    if (it.second.size() - 1 == '/')
      it.second = it.second.substr(0, it.second.size() - 1);
  return result;
}
