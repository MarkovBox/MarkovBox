# Project Name
TARGET = MarkovBox

# Sources
CPP_SOURCES = main.cpp

# Library Locations
LIBDAISY_DIR = ./libDaisy/
DAISYSP_DIR = ./DaisySP/

# PC build configuration
PC_BUILD_DIR = build_pc
PC_TARGET = $(PC_BUILD_DIR)/$(TARGET)
PC_CXX = g++
PC_CXXFLAGS = -std=gnu++17 -O2 -Wall -Wextra -I$(DAISYSP_DIR)/Source -I$(DAISYSP_DIR)/Source/Utility
PC_SOURCES = main_pc.cpp $(DAISYSP_DIR)/Source/Synthesis/oscillator.cpp

.PHONY: pc clean-pc

pc: $(PC_TARGET)

$(PC_TARGET): $(PC_SOURCES) | $(PC_BUILD_DIR)
	$(PC_CXX) $(PC_CXXFLAGS) $(PC_SOURCES) -o $@

$(PC_BUILD_DIR):
	mkdir -p $@

clean-pc:
	rm -rf $(PC_BUILD_DIR)

SYSTEM_FILES_DIR = $(LIBDAISY_DIR)/core
include $(SYSTEM_FILES_DIR)/Makefile
