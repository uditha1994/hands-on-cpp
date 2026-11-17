# Ruwan Stores Manager

The capstone project from Chapter 17 of *Hands-On C++*: a console application that manages a small shop's inventory, records sales and saves everything to CSV files.

## Build and run

```bash
make            # or: g++ -std=c++17 -Wall -Wextra product.cpp inventory.cpp input.cpp main.cpp -o shop
./shop
```

On Windows, run `shop.exe`. The program reads and writes `inventory.csv` in the folder you run it from, and appends each sale to `sales.csv`.

## Files

| File | Purpose |
|---|---|
| `product.h`, `product.cpp` | The `Product` struct and conversion to and from one CSV line |
| `inventory.h`, `inventory.cpp` | Loading, saving, finding, searching and printing products |
| `input.h`, `input.cpp` | Validated keyboard input |
| `main.cpp` | The menu and one function per menu option |
| `inventory.csv` | Sample data to start with |

The ideas used here are explained in Chapters 9 to 17 of the book. The "Make it yours" project at the end of Chapter 17 lists extensions to try.
