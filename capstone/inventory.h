#ifndef INVENTORY_H
#define INVENTORY_H

#include <string>
#include <vector>
#include "product.h"

bool loadInventory(const std::string &filename, std::vector<Product> &items);
bool saveInventory(const std::string &filename, const std::vector<Product> &items);
int findByCode(const std::vector<Product> &items, const std::string &code);
std::vector<int> searchByName(const std::vector<Product> &items, const std::string &text);
void printTable(const std::vector<Product> &items);
double stockValue(const std::vector<Product> &items);

#endif
