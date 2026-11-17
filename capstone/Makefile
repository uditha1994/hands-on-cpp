CXX ?= g++
CXXFLAGS ?= -std=c++17 -Wall -Wextra
SRCS = product.cpp inventory.cpp input.cpp main.cpp
OBJS = $(SRCS:.cpp=.o)

shop: $(OBJS)
	$(CXX) $(CXXFLAGS) $(OBJS) -o shop

%.o: %.cpp product.h inventory.h input.h
	$(CXX) $(CXXFLAGS) -c $< -o $@

.PHONY: clean
clean:
	rm -f $(OBJS) shop
