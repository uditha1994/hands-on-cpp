#ifndef PRODUCT_H
#define PRODUCT_H

#include <string>

struct Product {
    std::string code;
    std::string name;
    double price = 0.0;
    int stock = 0;
};

// Converts a product to one CSV line, and back again.
std::string toCsv(const Product &p);
bool fromCsv(const std::string &line, Product &p);

#endif
