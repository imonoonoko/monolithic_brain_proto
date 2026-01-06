import llama_cpp
import os
import sys

# Output purely the lib directory path for batch consumption
lib_path = os.path.join(os.path.dirname(llama_cpp.__file__), "lib")
print(lib_path)
