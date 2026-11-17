# Hands-On C++ build targets
#   make verify   compile and run every C++ example in the book
#   make web      build dist/Hands-On_Cpp_Handbook.html
#   make pdf      build dist/Hands-On_Cpp_Uditha_Landekumbura.pdf
#   make all      verify, then build both outputs

export PATH := $(CURDIR)/node_modules/.bin:$(PATH)
PY ?= python3

.PHONY: all setup verify web pdf capstone clean

all: verify web pdf

setup:
	$(PY) -m pip install -r requirements.txt
	npm install
	npx playwright install chromium

verify:
	HB_NO_FLOW=1 $(PY) tools/build.py verify
	$(PY) tools/verify.py

web:
	$(PY) tools/build.py web

pdf:
	tools/make_pdf.sh

capstone:
	$(MAKE) -C capstone

clean:
	rm -rf build .cache
	$(MAKE) -C capstone clean
