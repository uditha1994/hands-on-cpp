#include "inventory.h"
#include <fstream>
#include <iostream>
#include <iomanip>
#include <cctype>
using namespace std;

bool loadInventory(const string &filename, vector<Product> &items) {
    ifstream in(filename);
    if (!in) return false;
    items.clear();
    string line;
    getline(in, line);                        // skip the header
    int lineNo = 1;
    while (getline(in, line)) {
        lineNo++;
        if (line.empty()) continue;
        Product p;
        if (fromCsv(line, p)) {
            items.push_back(p);
        } else {
            cout << "Warning: skipped bad line " << lineNo << " in " << filename << endl;
        }
    }
    return true;
}

bool saveInventory(const string &filename, const vector<Product> &items) {
    ofstream out(filename);
    if (!out) return false;
    out << "code,name,price,stock\n";
    for (const Product &p : items) out << toCsv(p) << "\n";
    return true;
}

int findByCode(const vector<Product> &items, const string &code) {
    for (size_t i = 0; i < items.size(); i++) {
        if (items[i].code == code) return i;
    }
    return -1;
}

static string lower(string s) {               // static: only visible in this file
    for (char &c : s) c = tolower(static_cast<unsigned char>(c));
    return s;
}

vector<int> searchByName(const vector<Product> &items, const string &text) {
    vector<int> hits;
    string t = lower(text);
    for (size_t i = 0; i < items.size(); i++) {
        if (lower(items[i].name).find(t) != string::npos) hits.push_back(i);
    }
    return hits;
}

void printTable(const vector<Product> &items) {
    cout << left << setw(8) << "Code" << setw(22) << "Name" << right << setw(10) << "Price"
         << setw(7) << "Stock" << endl;
    cout << string(47, '-') << endl;
    cout << fixed << setprecision(2);
    for (const Product &p : items) {
        cout << left << setw(8) << p.code << setw(22) << p.name << right << setw(10) << p.price
             << setw(7) << p.stock << (p.stock < 10 ? "  LOW" : "") << endl;
    }
}

double stockValue(const vector<Product> &items) {
    double total = 0;
    for (const Product &p : items) total += p.price * p.stock;
    return total;
}
