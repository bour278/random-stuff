import sys

# Create sample dictionaries
dict1 = {'a': 1, 'b': 2}
dict2 = {'c': 3, 'd': 4}

# Print memory addresses before merging
print("Memory addresses before merging:")
print(f"dict1 at {id(dict1)}")
print(f"dict1['a'] at {id(dict1['a'])}")
print(f"dict2 at {id(dict2)}")
print(f"dict2['c'] at {id(dict2['c'])}")

# Different ways to merge dictionaries
# 1. Using update()
merged1 = dict1.copy()  # Creates new dict object
merged1.update(dict2)   # Modifies merged1 in-place

# 2. Using | operator (Python 3.9+)
merged2 = dict1 | dict2  # Creates new dict object

# 3. Using dictionary unpacking
merged3 = {**dict1, **dict2}  # Creates new dict object

# Print memory addresses after merging
print("\nMemory addresses after merging:")
print(f"merged1 at {id(merged1)}")
print(f"merged2 at {id(merged2)}")
print(f"merged3 at {id(merged3)}")

# Demonstrate reference sharing for nested dictionaries
nested_dict1 = {'x': {'nested': 'value'}}
nested_dict2 = {'y': 42}
merged_nested = nested_dict1 | nested_dict2

print("\nNested dictionary references:")
print(f"Original nested dict at {id(nested_dict1['x'])}")
print(f"Merged nested dict at {id(merged_nested['x'])}")
print("Note: They share the same memory address!")

# Memory size comparison
print("\nMemory sizes:")
print(f"dict1 size: {sys.getsizeof(dict1)} bytes")
print(f"dict2 size: {sys.getsizeof(dict2)} bytes")
print(f"merged1 size: {sys.getsizeof(merged1)} bytes")
