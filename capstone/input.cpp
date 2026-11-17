#include "input.h"
#include <iostream>
#include <limits>
#include <cstdlib>
using namespace std;

int readInt(const string &prompt, int low, int high) {
    int value;
    while (true) {
        cout << prompt;
        if (cin >> value && value >= low && value <= high) {
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            return value;
        }
        if (cin.eof()) exit(1);               // no more input at all: stop
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        cout << "Please enter a whole number from " << low << " to " << high << "." << endl;
    }
}

double readDouble(const string &prompt, double low) {
    double value;
    while (true) {
        cout << prompt;
        if (cin >> value && value >= low) {
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            return value;
        }
        if (cin.eof()) exit(1);
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        cout << "Please enter a number of at least " << low << "." << endl;
    }
}

string readLine(const string &prompt) {
    string s;
    cout << prompt;
    getline(cin, s);
    return s;
}
