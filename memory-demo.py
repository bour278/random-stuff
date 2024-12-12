from pympler import summary, muppy, asizeof
from memory_profiler import profile
import tracemalloc
from gc import get_referents
import ctypes

def print_hex_addresses(obj, name="object"):
    """Print hex addresses of an object and its contents."""
    print(f"\n{name.upper()} MEMORY ADDRESSES:")
    print(f"Main object at: 0x{id(obj):016x}")
    
    if isinstance(obj, dict):
        print("\nContents:")
        for k, v in obj.items():
            print(f"Key {k!r:>8} at: 0x{id(k):016x}")
            print(f"Value {v!r:>6} at: 0x{id(v):016x}")
            if hasattr(k, '__dict__') or hasattr(v, '__dict__'):
                print(f"{'─' * 20}")

# Start memory tracking
tracemalloc.start()

# Create and analyze original dictionaries
dict1 = {'a': 1, 'b': 2}
dict2 = {'c': 3, 'd': 4}

print_hex_addresses(dict1, "dict1")
print_hex_addresses(dict2, "dict2")

# Take first snapshot
snapshot1 = tracemalloc.take_snapshot()

# Perform merge operations
merged_pipe = dict1 | dict2
merged_update = dict1.copy()
merged_update.update(dict2)
merged_unpack = {**dict1, **dict2}

# Take second snapshot
snapshot2 = tracemalloc.take_snapshot()

print_hex_addresses(merged_pipe, "merged dictionary")

print("\nMEMORY ALLOCATION DIFFERENCES:")
stats = snapshot2.compare_to(snapshot1, 'lineno')
for stat in stats[:3]:
    print(stat)

print("\nDETAILED SIZE ANALYSIS:")
print(f"dict1 size:        {asizeof.asizeof(dict1):,} bytes at 0x{id(dict1):016x}")
print(f"dict2 size:        {asizeof.asizeof(dict2):,} bytes at 0x{id(dict2):016x}")
print(f"merged_pipe size:  {asizeof.asizeof(merged_pipe):,} bytes at 0x{id(merged_pipe):016x}")

print("\nMEMORY MAPPED OBJECTS:")
all_objects = muppy.get_objects()
sum1 = summary.summarize(all_objects)
summary.print_(sum1)

def show_refs_with_addr(obj, level=0, seen=None):
    """Show reference tree with memory addresses."""
    if seen is None:
        seen = set()
    
    obj_id = id(obj)
    if obj_id in seen:
        print("  " * level + f"0x{obj_id:016x} {type(obj).__name__}: <circular reference>")
        return
    seen.add(obj_id)
    
    print("  " * level + f"0x{obj_id:016x} {type(obj).__name__}: {obj!r}")
    
    # Get referents for container types
    if isinstance(obj, (dict, list, tuple, set)):
        for ref in get_referents(obj):
            if isinstance(ref, (dict, list, tuple, set, int, str, float)):
                show_refs_with_addr(ref, level + 1, seen)

print("\nREFERENCE TREE WITH ADDRESSES:")
show_refs_with_addr(merged_pipe)

# Memory block information
print("\nMEMORY BLOCK INFORMATION:")
for dict_obj in [dict1, dict2, merged_pipe]:
    size = asizeof.asizeof(dict_obj)
    print(f"\nDictionary at 0x{id(dict_obj):016x}:")
    print(f"Size: {size:,} bytes")
    print(f"References: {sys.getrefcount(dict_obj) - 1}")  # Subtract 1 for the getrefcount call
    
# Stop tracking
tracemalloc.stop()
