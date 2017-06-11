CXX = g++
CPPFLAGS = -DDEBUG
CXXFLAGS = -o3 -std=c++11 -Wall -Wextra -Wconversion
SANITIZER = -fsanitize=address
LDFLAGS = -ljpeg

TARGET main
OBJS = main.o image.o assignment6.o
INCS = image.hpp boost/multi_array.hpp

$(TARGET): $(OBJS)
	$(CXX) -o $(TARGET) $(OBJS) $(LDFLAGS)
	
%.o %.cpp $(INCS)
	$(CXX) -c -o $@ $< $(CPPFLAGS) $(CXXFLAGS) $(SANITIZER)
	
clean:
	rm -f $(OBJS) $(TARGET) *~
	
run: $(TARGET)
	./$(TARGET)