#include <iostream>
#include <iomanip>
#include <fstream>
#include <vector>
#include <algorithm>
#include "product.h"
#include "inventory.h"
#include "input.h"
using namespace std;

const string DATA_FILE = "inventory.csv";
const string SALES_FILE = "sales.csv";

void listProducts(vector<Product> &items) {
    int order = readInt("Sort by 1) code 2) name 3) price 4) stock: ", 1, 4);
    switch (order) {
        case 1: sort(items.begin(), items.end(), [](const Product &a, const Product &b) { return a.code < b.code; }); break;
        case 2: sort(items.begin(), items.end(), [](const Product &a, const Product &b) { return a.name < b.name; }); break;
        case 3: sort(items.begin(), items.end(), [](const Product &a, const Product &b) { return a.price < b.price; }); break;
        case 4: sort(items.begin(), items.end(), [](const Product &a, const Product &b) { return a.stock < b.stock; }); break;
    }
    printTable(items);
    cout << "Stock value: Rs. " << fixed << setprecision(2) << stockValue(items) << endl;
}

void searchProducts(const vector<Product> &items) {
    string text = readLine("Search for: ");
    vector<Product> found;
    for (int i : searchByName(items, text)) found.push_back(items[i]);
    if (found.empty()) cout << "Nothing matches \"" << text << "\"." << endl;
    else printTable(found);
}

void addProduct(vector<Product> &items) {
    Product p;
    p.code = readLine("New code: ");
    if (p.code.empty() || findByCode(items, p.code) != -1) {
        cout << "That code is empty or already used." << endl;
        return;
    }
    p.name = readLine("Name: ");
    if (p.name.find(',') != string::npos) {
        cout << "Names cannot contain commas." << endl;
        return;
    }
    p.price = readDouble("Price (Rs.): ", 0.01);
    p.stock = readInt("Opening stock: ", 0, 100000);
    items.push_back(p);
    cout << "Added " << p.name << "." << endl;
}

void recordSale(vector<Product> &items) {
    int i = findByCode(items, readLine("Product code: "));
    if (i == -1) {
        cout << "No product with that code." << endl;
        return;
    }
    Product &p = items[i];                       // a reference: changes go into the vector
    if (p.stock == 0) {
        cout << p.name << " is out of stock." << endl;
        return;
    }
    int qty = readInt("Quantity (1-" + to_string(p.stock) + "): ", 1, p.stock);
    p.stock -= qty;
    double total = qty * p.price;
    ofstream log(SALES_FILE, ios::app);
    if (log) log << p.code << "," << qty << "," << fixed << setprecision(2) << total << "\n";
    cout << "Sold " << qty << " x " << p.name << " = Rs. " << fixed << setprecision(2) << total << endl;
}

void restock(vector<Product> &items) {
    int i = findByCode(items, readLine("Product code: "));
    if (i == -1) {
        cout << "No product with that code." << endl;
        return;
    }
    items[i].stock += readInt("Quantity received: ", 1, 100000);
    cout << items[i].name << " now has " << items[i].stock << " in stock." << endl;
}

void lowStockReport(const vector<Product> &items) {
    vector<Product> low;
    for (const Product &p : items) {
        if (p.stock < 10) low.push_back(p);
    }
    if (low.empty()) cout << "All products are well stocked." << endl;
    else printTable(low);
}

int main() {
    vector<Product> items;
    if (!loadInventory(DATA_FILE, items)) {
        cout << "No " << DATA_FILE << " yet. Starting with an empty inventory." << endl;
    }
    cout << "=== RUWAN STORES MANAGER ===  (" << items.size() << " products loaded)" << endl;

    int choice;
    do {
        cout << "\n1 List  2 Search  3 Add  4 Sale  5 Restock  6 Low stock  0 Save and exit" << endl;
        choice = readInt("Choice: ", 0, 6);
        switch (choice) {
            case 1: listProducts(items); break;
            case 2: searchProducts(items); break;
            case 3: addProduct(items); break;
            case 4: recordSale(items); break;
            case 5: restock(items); break;
            case 6: lowStockReport(items); break;
            case 0: break;
        }
    } while (choice != 0);

    if (saveInventory(DATA_FILE, items)) cout << "Saved " << items.size() << " products. Goodbye!" << endl;
    else cout << "ERROR: could not save " << DATA_FILE << endl;
    return 0;
}
