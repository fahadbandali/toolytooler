#!/bin/bash
# Enhanced script: Searches for duplicate FILE_TYPE files and deletes the file in the source directory.
# Use the --dry-run flag to only report the duplicate without deleting it.
#
# Usage:
#   ./check_duplicates.sh [--dry-run] --check <directory_to_check> --in <external_directory>
# ./check_duplicates.sh --dry-run --check /Users/fahadbandali/Downloads --in /Volumes/FBSTORAGE --type mp4

usage() {
    echo "Usage: $0 [--dry-run] --check <directory_to_check> --in <external_directory> --type"
    exit 1
}

# Default: do not delete
DRY_RUN=false

# Process command-line arguments
if [ "$#" -lt 4 ]; then
    usage
fi

while [ "$#" -gt 0 ]; do
    case "$1" in
        --dry-run)
            DRY_RUN=true
            shift 1
            ;;
        --check)
            CHECK_DIR="$2"
            shift 2
            ;;
        --in)
            EXTERNAL_DIR="$2"
            shift 2
            ;;
        --type)
            FILE_TYPE="*.$2"
            shift 2
            ;;
        *)
            echo "Unknown parameter: $1"
            usage
            ;;
    esac
done

# Validate input directories
if [ -z "$CHECK_DIR" ] || [ -z "$EXTERNAL_DIR" ]; then
    usage
fi

if [ ! -d "$CHECK_DIR" ]; then
    echo "Error: Directory to check ($CHECK_DIR) does not exist."
    exit 1
fi

if [ ! -d "$EXTERNAL_DIR" ]; then
    echo "Error: External directory ($EXTERNAL_DIR) does not exist."
    exit 1
fi

echo "Searching for duplicate $FILE_TYPE files from '$CHECK_DIR' in '$EXTERNAL_DIR'..."
if [ "$DRY_RUN" = true ]; then
    echo "Running in dry-run mode: No files will be deleted."
fi
echo "--------------------------------------------------------------"

# Loop through all FILE_TYPE files in the check directory (case insensitive)
find "$CHECK_DIR" -type f -iname "*.$FILE_TYPE" -print0 | while IFS= read -r -d '' file; do
    filename=$(basename "$file")
    
    # Use -xdev to restrict find on the external drive to the same filesystem
    duplicate=$(find "$EXTERNAL_DIR" -xdev -type f -iname "$filename" -print -quit 2>/dev/null)
    
    if [ -n "$duplicate" ]; then
        echo "Duplicate found:"
        echo "  Source:    $file"
        echo "  Duplicate: $duplicate"
        if [ "$DRY_RUN" = true ]; then
            echo "Dry-run: Would delete '$file'"
        else
            rm "$file" && echo "Deleted '$file'" || echo "Failed to delete '$file'"
        fi
    fi
done
