from pympler import summary, muppy, asizeof
from memory_profiler import profile
import tracemalloc
from gc import get_referents
import ctypes
import sys
from IPython.display import display, HTML, Markdown
from typing import Any
import json

def color_hex(hex_str: str) -> str:
    """Format hex address in orange."""
    return f"\033[38;5;214m{hex_str}\033[0m"

def color_dict(d: dict) -> str:
    """Format dictionary content in cyan."""
    return f"\033[36m{d}\033[0m"

def color_size(size: int) -> str:
    """Format size in green."""
    return f"\033[32m{size:,} bytes\033[0m"

def print_memory_state(name: str, obj: Any, detailed: bool = True):
    """Print detailed memory state with colors."""
    display(Markdown(f"## {name}"))
    
    # Basic information
    print(f"Address: {color_hex(f'0x{id(obj):016x}')}")
    print(f"Size: {color_size(asizeof.asizeof(obj))}")
    print(f"Type: \033[35m{type(obj).__name__}\033[0m")
    
    if isinstance(obj, dict):
        print("\nContent:")
        print(color_dict(json.dumps(obj, indent=2)))
        
        if detailed:
            print("\nDetailed memory layout:")
            for k, v in obj.items():
                print(f"\nKey: \033[33m{k!r}\033[0m")
                print(f"  ├─ Address: {color_hex(f'0x{id(k):016x}')}")
                print(f"  ├─ Size: {color_size(asizeof.asizeof(k))}")
                print(f"  ├─ Hash: {color_hex(f'0x{hash(k):016x}')}")
                print(f"Value: \033[34m{v!r}\033[0m")
                print(f"  ├─ Address: {color_hex(f'0x{id(v):016x}')}")
                print(f"  └─ Size: {color_size(asizeof.asizeof(v))}")

def show_memory_changes(snapshot1, snapshot2, title: str):
    """Show memory differences between snapshots."""
    display(Markdown(f"## {title}"))
    stats = snapshot2.compare_to(snapshot1, 'lineno')
    for stat in stats[:3]:
        size = stat.size_diff
        count = stat.count_diff
        print(f"\033[{'32' if size >= 0 else '31'}m{size:+,} bytes\033[0m", end=' ')
        print(f"({'+'if count >= 0 else ''}{count:,} objects)")
        print(f"  {stat.traceback.format()[-1]}")

# Start tracking memory
tracemalloc.start()

# Create initial dictionaries
dict1 = {'a': 1, 'b': 2}
dict2 = {'c': 3, 'd': 4}

print_memory_state("Initial Dictionary 1", dict1)
print_memory_state("Initial Dictionary 2", dict2)

# Take first snapshot
snapshot1 = tracemalloc.take_snapshot()

display(Markdown("# Merging Operations"))

# Method 1: Update
display(Markdown("## Method 1: Update"))
merged_update = dict1.copy()
snapshot_pre_update = tracemalloc.take_snapshot()
merged_update.update(dict2)
snapshot_post_update = tracemalloc.take_snapshot()
print_memory_state("After update()", merged_update)
show_memory_changes(snapshot_pre_update, snapshot_post_update, "Memory Changes during update()")

# Method 2: Pipe operator
display(Markdown("## Method 2: Pipe Operator"))
snapshot_pre_pipe = tracemalloc.take_snapshot()
merged_pipe = dict1 | dict2
snapshot_post_pipe = tracemalloc.take_snapshot()
print_memory_state("After pipe operator", merged_pipe)
show_memory_changes(snapshot_pre_pipe, snapshot_post_pipe, "Memory Changes during pipe operation")

# Method 3: Dictionary unpacking
display(Markdown("## Method 3: Dictionary Unpacking"))
snapshot_pre_unpack = tracemalloc.take_snapshot()
merged_unpack = {**dict1, **dict2}
snapshot_post_unpack = tracemalloc.take_snapshot()
print_memory_state("After unpacking", merged_unpack)
show_memory_changes(snapshot_pre_unpack, snapshot_post_unpack, "Memory Changes during unpacking")

# Reference tree visualization
def print_ref_tree(obj, level=0, seen=None):
    """Print reference tree with colored formatting."""
    if seen is None:
        seen = set()
    
    obj_id = id(obj)
    if obj_id in seen:
        print("  " * level + f"{color_hex(f'0x{obj_id:016x}')} \033[31m<circular reference>\033[0m")
        return
    seen.add(obj_id)
    
    type_name = f"\033[35m{type(obj).__name__}\033[0m"
    print("  " * level + f"{color_hex(f'0x{obj_id:016x}')} {type_name}: {color_dict(str(obj))}")
    
    if isinstance(obj, (dict, list, tuple, set)):
        for ref in get_referents(obj):
            if isinstance(ref, (dict, list, tuple, set, int, str, float)):
                print_ref_tree(ref, level + 1, seen)

display(Markdown("# Reference Trees"))
print("\nMerged dictionary reference tree:")
print_ref_tree(merged_pipe)

# Memory summary
display(Markdown("# Final Memory Summary"))
print(f"\nTotal memory used by dictionaries:")
print(f"dict1: {color_size(asizeof.asizeof(dict1))}")
print(f"dict2: {color_size(asizeof.asizeof(dict2))}")
print(f"merged_update: {color_size(asizeof.asizeof(merged_update))}")
print(f"merged_pipe: {color_size(asizeof.asizeof(merged_pipe))}")
print(f"merged_unpack: {color_size(asizeof.asizeof(merged_unpack))}")

# Stop tracking
tracemalloc.stop()

# Cleanup
del snapshot1, snapshot_pre_update, snapshot_post_update
del snapshot_pre_pipe, snapshot_post_pipe
del snapshot_pre_unpack, snapshot_post_unpack
