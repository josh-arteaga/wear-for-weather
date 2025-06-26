import os
import argparse

DEFAULT_IGNORE_DIRS = {
    'node_modules', 'venv', '__pycache__', '.git', '.idea', 'dist', 'build',
    'target', 'out', 'bin', 'obj', 'packages', 'vendor', 'coverage', 'logs',
    '.expo'
}

def generate_tree(
    root_path,
    prefix='',
    is_last=True,
    ignore_dirs=None,
    ignore_hidden=True,
    max_file_size=None,
    output_file=None
):
    """Recursively generate directory tree with visual structure"""
    if ignore_dirs is None:
        ignore_dirs = DEFAULT_IGNORE_DIRS

    # Get display name for root
    base = os.path.basename(root_path)
    if not base:  # Handle root directory (e.g., '/')
        base = os.path.dirname(root_path)

    # Format the Root entry
    line = prefix + ('└── ' if is_last else '├── ') + base

    # Write to file if specified
    if output_file:
        output_file.write(line + '\n')

    # New prefix components for children
    extension = '    ' if is_last else '│   '
    new_prefix = prefix + extension

    try:
        entries = os.listdir(root_path)
    except (PermissionError, OSError):
        return

    # Filter and sort entries
    valid_entries = []
    for name in entries:
        if ignore_hidden and name.startswith('.'):
            continue
            
        full_path = os.path.join(root_path, name)
        
        if os.path.isdir(full_path):
            if name in ignore_dirs:
                continue
            valid_entries.append((name, 'dir'))
        else:  # File
            if max_file_size:
                try:
                    if os.path.getsize(full_path) > max_file_size:
                        continue
                except OSError:
                    pass  # Skip if we can't check size
            valid_entries.append((name, 'file'))
    
    # Sort directories first then files, both alphabetically
    valid_entries.sort(key=lambda x: (x[1] != 'dir', x[0].lower()))
    
    # Process each entry
    for i, (name, entry_type) in enumerate(valid_entries):
        is_last_entry = (i == len(valid_entries) - 1)
        full_path = os.path.join(root_path, name)
        
        if entry_type == 'dir':
            yield from generate_tree(
                full_path,
                prefix=new_prefix,
                is_last=is_last_entry,
                ignore_dirs=ignore_dirs,
                ignore_hidden=ignore_hidden,
                max_file_size=max_file_size,
                output_file=output_file
            )
        else:  # File
            line = new_prefix + new_prefix + ('└── ' if is_last_entry else '├── ') + name
            if output_file:
                output_file.write(line + '\n')
            yield line

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate file tree excluding package directories and large files.')
    parser.add_argument('root', nargs='?', default='.', help='Root directory (default: current dir)')
    parser.add_argument('--ignore-dirs', nargs='*', default=DEFAULT_IGNORE_DIRS, help='Directories to exclude')
    parser.add_argument('--no-ignore-hidden', dest='ignore_hidden', action='store_false', help='Include hidden files/dirs')
    parser.add_argument('--max-file-size', type=int, default=1024*1024, help='Max file size in bytes (default: 1MB)')
    parser.add_argument('--output', type=str, help='Output file to save tree (default: print to console)')
    
    args = parser.parse_args()
    args.ignore_dirs = set(args.ignore_dirs)  # Ensure set type
    root_path = os.path.abspath(args.root)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            for _ in generate_tree(
                root_path,
                prefix='',
                is_last=True,
                ignore_dirs=args.ignore_dirs,
                max_file_size=args.max_file_size,
                output_file=f
            ):
                pass
        print(f" 👍 File tree saved to: {os.path.abspath(args.output)} 🌳 ")
    else:
        for line in generate_tree(
            os.path.abspath(args.root),
            prefix='',
            is_last=True,
            ignore_dirs=args.ignore_dirs,
            ignore_hidden=args.ignore_hidden,
            max_file_size=args.max_file_size
        ):
            print(line)