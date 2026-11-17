#include "product.h"
#include <sstream>
#include <iomanip>
using namespace std;

string toCsv(const Product &p) {
    ostringstream out;
    out << p.code << "," << p.name << "," << fixed << setprecision(2) << p.price << "," << p.stock;
    return out.str();
}

bool fromCsv(const string &line, Product &p) {
    istringstream in(line);
    string priceText, stockText;
    if (!getline(in, p.code, ',')) return false;
    if (!getline(in, p.name, ',')) return false;
    if (!getline(in, priceText, ',')) return false;
    if (!getline(in, stockText, ',')) return false;
    try {
        p.price = stod(priceText);
        p.stock = stoi(stockText);
    } catch (...) {          // a corrupted number: reject this line
        return false;
    }
    return true;
}
