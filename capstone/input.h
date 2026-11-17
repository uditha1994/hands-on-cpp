#ifndef INPUT_H
#define INPUT_H

#include <string>

int readInt(const std::string &prompt, int low, int high);
double readDouble(const std::string &prompt, double low);
std::string readLine(const std::string &prompt);

#endif
