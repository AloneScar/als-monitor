XX = g++
TAGET = main

SRC_DIR = ./src # save .cpp file
BUILD_DIR = ./build # save .o file
TAGET_DIR = ./target # save exec file
TAGET_FILE = $(shell echo '$(TAGET_DIR)$(TAGET)' | awk '{gsub(/ /, "/"); print $$0}')
INCLUDE_DIR = ./include # save .h file


SRCS = $(shell ls $(SRC_DIR) | grep .cpp | awk '{print "$(SRC_DIR)"$$0}' | awk '{ gsub(/ /, "/"); print $$0}')
INCLUDES = $(shell ls $(INCLUDE_DIR) | grep .cpp | awk '{print "$(INCLUDE_DIR)"$$0}' | awk '{ gsub(/ /, "/"); print $$0}')
OBJS = $(shell ls $(SRC_DIR) | grep .cpp | awk '{print "$(BUILD_DIR)"$$0}' | awk '{ gsub(/ /, "/"); print $$0}' | awk '{ gsub(/.cpp/, ".o"); print $$0 }')
SRCS_FRONT_NAME = $(shell ls $(SRC_DIR) | grep .cpp | awk '{gsub(/.cpp/, ""); print $$0}')

CXXFLAGS = -Wall -I $(INCLUDE_DIR)

$(TAGET_FILE): $(OBJS)
	$(CXX) -o $@ $^

$(OBJS): $(SRCS) $(INCLUDES)
	$(foreach name, $(SRCS_FRONT_NAME), \
		$(shell $(CXX) $(CXXFLAGS) -c \
		$(shell echo $(SRC_DIR)$(name).cpp | awk '{gsub(/ /, "/"); print $$0}') -o \
		$(shell echo $(BUILD_DIR)/$(name).o | awk '{gsub(/ /, "/"); print $$0}')))

.PHONY:clean
clean:
	rm -rf $(BUILD_DIR) $(TAGET_DIR)
	mkdir $(BUILD_DIR) $(TAGET_DIR)

.PHONY:init
init:
	mkdir res target include src build

.PHONY:run
run:
	$(TAGET_FILE)
