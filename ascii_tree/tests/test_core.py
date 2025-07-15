#!/usr/bin/env python

import pytest

from ascii_tree import ascii_tree

###############################################################################

LIST_OF_PATHS_INPUT = [
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

NO_LIMITS_FROM_LIST = """
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
""".strip()

DEPTH_2_FROM_LIST = """
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
""".strip()

MAX_FILES_2_MAX_DIRS_1_FROM_LIST = """
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
""".strip()

MAX_FILES_3_FROM_LIST = """
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
""".strip()


@pytest.mark.parametrize(
    "paths, max_depth, max_files_per_dir, max_dirs_per_dir, expected_output",
    [
        (LIST_OF_PATHS_INPUT, None, None, None, NO_LIMITS_FROM_LIST),
        (LIST_OF_PATHS_INPUT, 2, None, None, DEPTH_2_FROM_LIST),
        (LIST_OF_PATHS_INPUT, None, 2, 1, MAX_FILES_2_MAX_DIRS_1_FROM_LIST),
        (LIST_OF_PATHS_INPUT, None, 3, None, MAX_FILES_3_FROM_LIST),
    ],
)
def test_paths_to_tree(
    paths: list[str],
    max_depth: int,
    max_files_per_dir: int,
    max_dirs_per_dir: int,
    expected_output: str,
) -> None:
    result = ascii_tree(
        paths,
        max_depth=max_depth,
        max_files_per_dir=max_files_per_dir,
        max_dirs_per_dir=max_dirs_per_dir,
    )
    assert result == expected_output


###############################################################################


DICT_OF_PATHS_INPUT = {
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

SHOW_FILE_SIZES_FROM_DICT = """
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
""".strip()

SORTED_SIZES_MAX_FILES_2_MAX_DIRS_1_FROM_DICT = """
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
""".strip()

SORTED_SIZES_MAX_DEPTH_4_MAX_FILES_3_MAX_DIRS_1_FROM_DICT = """
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
""".strip()


@pytest.mark.parametrize(
    (
        "paths, max_depth, max_files_per_dir, max_dirs_per_dir, "
        "sort_by_size, show_sizes, expected_output"
    ),
    [
        (DICT_OF_PATHS_INPUT, None, None, None, False, True, SHOW_FILE_SIZES_FROM_DICT),
        (
            DICT_OF_PATHS_INPUT,
            None,
            2,
            1,
            True,
            True,
            SORTED_SIZES_MAX_FILES_2_MAX_DIRS_1_FROM_DICT,
        ),
        (
            DICT_OF_PATHS_INPUT,
            4,
            3,
            1,
            True,
            True,
            SORTED_SIZES_MAX_DEPTH_4_MAX_FILES_3_MAX_DIRS_1_FROM_DICT,
        ),
    ],
)
def test_paths_to_tree_with_dict(
    paths: dict[str, int],
    max_depth: int,
    max_files_per_dir: int,
    max_dirs_per_dir: int,
    sort_by_size: bool,
    show_sizes: bool,
    expected_output: str,
) -> None:
    result = ascii_tree(
        paths,
        max_depth=max_depth,
        max_files_per_dir=max_files_per_dir,
        max_dirs_per_dir=max_dirs_per_dir,
        sort_by_size=sort_by_size,
        show_sizes=show_sizes,
    )
    assert result == expected_output
