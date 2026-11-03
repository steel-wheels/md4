#
# Makefile
#

PREFIX_DIR	= /usr/local
BIN_DIR		= $(PREFIX_DIR)/bin
LIB_DIR		= $(PREFIX_DIR)/libexec

all:
	@echo "make [install]"

install: $(BIN_DIR)/md4 $(LIB_DIR)/md4.py

$(BIN_DIR)/md4: ./src/md4.sh
	sudo install -m 555 $< $@

$(LIB_DIR)/md4.py: ./src/md4.py
	sudo install -m 444 $< $@

