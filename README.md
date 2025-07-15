# ASCII Tree from Paths

Create ASCII tree strings from list or directories of filepaths.
Useful for formatting directory information into LLM context window.

## Example usage

### Basic Usage with Strings

```python
example_paths = [
    "src/main.py",
    "src/utils/helpers.py",
    "src/utils/config.py",
    "src/utils/database.py",
    "src/utils/auth.py",
    "src/models/user.py",
    "src/models/database.py",
    "tests/test_main.py",
    "tests/test_utils.py",
    "tests/integration/test_api.py",
    "tests/integration/test_db.py",
    "docs/README.md",
    "docs/api/endpoints.md",
    "docs/api/authentication.md",
    "requirements.txt",
    ".gitignore",
]

print("1. Basic tree (no limits):")
print(paths_to_tree(example_paths))
print("\n" + "=" * 60 + "\n")

print("2. With depth limit (max_depth=2):")
print(paths_to_tree(example_paths, max_depth=2))
print("\n" + "=" * 60 + "\n")

print("3. With separate file and directory limits (max_files_per_dir=2, max_dirs_per_dir=1):")
print(paths_to_tree(example_paths, max_files_per_dir=2, max_dirs_per_dir=1))
print("\n" + "=" * 60 + "\n")

print("4. With file limit only (max_files_per_dir=3):")
print(paths_to_tree(example_paths, max_files_per_dir=3))
print("\n" + "=" * 60 + "\n")
```

**Output:**

```
1. Basic tree (no limits):
├── src
│   ├── utils
│   │   ├── helpers.py
│   │   ├── config.py
│   │   ├── database.py
│   │   └── auth.py
│   ├── models
│   │   ├── user.py
│   │   └── database.py
│   └── main.py
├── tests
│   ├── integration
│   │   ├── test_api.py
│   │   └── test_db.py
│   ├── test_main.py
│   └── test_utils.py
├── docs
│   ├── api
│   │   ├── endpoints.md
│   │   └── authentication.md
│   └── README.md
├── requirements.txt
└── .gitignore

============================================================

2. With depth limit (max_depth=2):
├── src
│   ├── utils
│   │   ├── ... (depth limit reached)
│   ├── models
│   │   ├── ... (depth limit reached)
│   └── main.py
├── tests
│   ├── integration
│   │   ├── ... (depth limit reached)
│   ├── test_main.py
│   └── test_utils.py
├── docs
│   ├── api
│   │   ├── ... (depth limit reached)
│   └── README.md
├── requirements.txt
└── .gitignore

============================================================

3. With separate file and directory limits (max_files_per_dir=2, max_dirs_per_dir=1):
├── src
│   ├── utils
│   │   ├── helpers.py
│   │   ├── config.py
│   │   └── ... (2 more files)
│   ├── main.py
│   └── ... (1 more directories)
├── requirements.txt
├── .gitignore
└── ... (2 more directories)

============================================================

4. With file limit only (max_files_per_dir=3):
├── src
│   ├── utils
│   │   ├── helpers.py
│   │   ├── config.py
│   │   ├── database.py
│   │   └── ... (1 more files)
│   ├── models
│   │   ├── user.py
│   │   └── database.py
│   └── main.py
├── tests
│   ├── integration
│   │   ├── test_api.py
│   │   └── test_db.py
│   ├── test_main.py
│   └── test_utils.py
├── docs
│   ├── api
│   │   ├── endpoints.md
│   │   └── authentication.md
│   └── README.md
├── requirements.txt
└── .gitignore
```


### Usage with Dictionary for Path and File Size

```python
path_sizes = {
    "src/main.py": 2048,
    "src/utils/helpers.py": 1024,
    "src/utils/config.py": 512,
    "src/utils/database.py": 4096,
    "src/utils/auth.py": 3072,
    "src/models/user.py": 1536,
    "tests/test_main.py": 2560,
    "README.md": 1024,
    "requirements.txt": 256,
}

print("5. With file sizes displayed:")
print(paths_to_tree(path_sizes, show_sizes=True))
print("\n" + "=" * 60 + "\n")

print("6. Sorted by size, 2 files per directory, 1 subdir per directory, sizes shown:")
print(
    paths_to_tree(
        path_sizes,
        max_files_per_dir=2,
        max_dirs_per_dir=1,
        sort_by_size=True,
        show_sizes=True,
    )
)
print("\n" + "=" * 60 + "\n")

print("7. All limits combined:")
print(
    paths_to_tree(
        path_sizes,
        max_depth=4,
        max_files_per_dir=3,
        max_dirs_per_dir=1,
        sort_by_size=True,
        show_sizes=True,
    )
)
```

**Output:**

```
============================================================

5. With file sizes displayed:
├── src
│   ├── utils
│   │   ├── helpers.py (1.0KB)
│   │   ├── config.py (512B)
│   │   ├── database.py (4.0KB)
│   │   └── auth.py (3.0KB)
│   ├── models
│   │   └── user.py (1.5KB)
│   └── main.py (2.0KB)
├── tests
│   └── test_main.py (2.5KB)
├── README.md (1.0KB)
└── requirements.txt (256B)

============================================================

6. Sorted by size, 2 files per directory, 1 subdir per directory, sizes shown:
├── src
│   ├── utils
│   │   ├── database.py (4.0KB)
│   │   ├── auth.py (3.0KB)
│   │   └── ... (2 more files)
│   ├── main.py (2.0KB)
│   └── ... (1 more directories)
├── README.md (1.0KB)
├── requirements.txt (256B)
└── ... (1 more directories)

============================================================

7. All limits combined:
├── src
│   ├── utils
│   │   ├── database.py (4.0KB)
│   │   ├── auth.py (3.0KB)
│   │   ├── helpers.py (1.0KB)
│   │   └── ... (1 more files)
│   ├── main.py (2.0KB)
│   └── ... (1 more directories)
├── README.md (1.0KB)
├── requirements.txt (256B)
└── ... (1 more directories)
```