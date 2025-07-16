#!/usr/bin/env python

from pathlib import Path

# ASCII tree components
SPACE = "    "
BRANCH = "│   "
TEE = "├── "
LAST = "└── "

###############################################################################


def build_tree_structure(paths: list[str] | dict[str, int]) -> dict:
    """Build a nested dictionary representing the directory tree structure."""
    tree: dict = {}

    # Handle both list of strings and dict of string->int
    path_items: list[tuple[str, int | None]]
    if isinstance(paths, dict):
        path_items = list(paths.items())
    else:
        path_items = [(path, None) for path in paths]

    for path_str, size in path_items:
        path = Path(path_str)
        parts = path.parts
        current = tree

        # Navigate through each part of the path
        for i, part in enumerate(parts):
            if part not in current:
                current[part] = {"_children": {}, "_size": None, "_is_file": False}

            # If this is the last part (the actual file/directory name)
            if i == len(parts) - 1:
                current[part]["_size"] = size
                current[part]["_is_file"] = True

            current = current[part]["_children"]

    return tree


def separate_dirs_and_files(items: list[tuple]) -> tuple[list[tuple], list[tuple]]:
    """
    Separate items into directories and files based on whether they have children.

    Returns
    -------
        (directories, files)
    """
    directories: list[tuple] = []
    files: list[tuple] = []

    for name, node_info in items:
        if node_info["_children"]:  # Has children, so it's a directory
            directories.append((name, node_info))
        else:  # No children, so it's a file
            files.append((name, node_info))

    return directories, files


def get_limited_items(
    items: list[tuple], max_items: int, sort_by_size: bool = False
) -> tuple[list[tuple], int]:
    """
    Get the items to display based on limits and sorting preferences.

    Returns
    -------
        (items_to_show, truncated_count)
    """
    if len(items) <= max_items:
        return items, 0

    if sort_by_size:
        # Sort by size (largest first), handling None sizes
        items_sorted = sorted(
            items, key=lambda x: x[1].get("_size", 0) or 0, reverse=True
        )
        return items_sorted[:max_items], len(items) - max_items
    else:
        # Just take the first items
        return items[:max_items], len(items) - max_items


def format_file_name(name: str, node_info: dict, show_sizes: bool = False) -> str:
    """Format the file/directory name with optional size information."""
    if show_sizes and node_info.get("_size") is not None:
        size: int = node_info["_size"]
        if size >= 1024 * 1024 * 1024:  # GB
            size_str = f"{size / (1024**3):.1f}GB"
        elif size >= 1024 * 1024:  # MB
            size_str = f"{size / (1024**2):.1f}MB"
        elif size >= 1024:  # KB
            size_str = f"{size / 1024:.1f}KB"
        else:
            size_str = f"{size}B"
        return f"{name} ({size_str})"
    return name


def render_tree(
    tree_dict: dict,
    prefix: str = "",
    max_depth: int | None = None,
    current_depth: int = 0,
    max_files_per_dir: int | None = None,
    max_dirs_per_dir: int | None = None,
    sort_by_size: bool = False,
    show_sizes: bool = False,
) -> list[str]:
    """Recursively render the tree structure as ASCII art."""
    lines = []

    # Check depth limit
    if max_depth is not None and current_depth >= max_depth:
        lines.append(prefix + TEE + "... (depth limit reached)")
        return lines

    items: list[tuple] = list(tree_dict.items())

    # Separate directories and files
    directories, files = separate_dirs_and_files(items)

    # Apply limits separately to directories and files
    dirs_to_show, dirs_truncated = (
        (directories, 0)
        if max_dirs_per_dir is None
        else get_limited_items(directories, max_dirs_per_dir, sort_by_size)
    )
    files_to_show, files_truncated = (
        (files, 0)
        if max_files_per_dir is None
        else get_limited_items(files, max_files_per_dir, sort_by_size)
    )

    # Combine directories and files for display (directories first)
    all_items_to_show = dirs_to_show + files_to_show
    total_truncated = dirs_truncated + files_truncated

    for i, (name, node_info) in enumerate(all_items_to_show):
        # Determine if this is the last item at this level (considering truncation)
        is_last = i == len(all_items_to_show) - 1 and total_truncated == 0

        # Choose the appropriate pointer
        pointer = LAST if is_last else TEE

        # Format the name with size if requested
        display_name = format_file_name(name, node_info, show_sizes)

        # Add the current item
        lines.append(prefix + pointer + display_name)

        # If there are subitems, recurse
        if node_info["_children"]:
            # Choose the appropriate extension for the prefix
            extension = SPACE if is_last else BRANCH
            lines.extend(
                render_tree(
                    node_info["_children"],
                    prefix + extension,
                    max_depth,
                    current_depth + 1,
                    max_files_per_dir,
                    max_dirs_per_dir,
                    sort_by_size,
                    show_sizes,
                )
            )

    # Add truncation notices if items were truncated
    if dirs_truncated > 0 or files_truncated > 0:
        truncation_messages = []
        if dirs_truncated > 0:
            truncation_messages.append(f"{dirs_truncated} more directories")
        if files_truncated > 0:
            truncation_messages.append(f"{files_truncated} more files")

        truncation_text = " and ".join(truncation_messages)
        pointer = LAST
        lines.append(prefix + pointer + f"... ({truncation_text})")

    return lines


def paths_to_tree(
    paths: list[str] | dict[str, int],
    max_depth: int | None = None,
    max_files_per_dir: int | None = None,
    max_dirs_per_dir: int | None = None,
    sort_by_size: bool = False,
    show_sizes: bool = False,
) -> str:
    """
    Convert a list of file paths or dict of paths->sizes to an ASCII tree.

    Args:
    ----
        paths: List of file path strings OR dict of path -> file size in bytes
        max_depth: Maximum depth to display (None for unlimited)
        max_files_per_dir: Maximum files per directory to display (None for unlimited)
        max_dirs_per_dir: Maximum subdirs per directory to display (None for unlimited)
        sort_by_size: If True and limits are set, show largest files/dirs first
        show_sizes: If True, display file sizes next to filenames (requires dict input)

    Returns:
    -------
        String containing the ASCII tree representation
    """
    if not paths:
        return ""

    # Build the tree structure
    tree_structure = build_tree_structure(paths)

    # Render the tree as ASCII art
    tree_lines = render_tree(
        tree_structure,
        max_depth=max_depth,
        max_files_per_dir=max_files_per_dir,
        max_dirs_per_dir=max_dirs_per_dir,
        sort_by_size=sort_by_size,
        show_sizes=show_sizes,
    )

    return "\n".join(tree_lines)
