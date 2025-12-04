#!/bin/bash

# =============================================================================
# Fess Documentation Version Creator
# =============================================================================
# This script creates a new version of the Fess documentation by:
# 1. Copying the previous version's documentation directories
# 2. Copying the previous version's image directories (for en and ja)
# 3. Replacing version numbers in all RST files
#
# Usage: ./create_version.sh <new_version>
# Example: ./create_version.sh 15.4
# =============================================================================

set -e

# Language directories to process
LANGUAGES=("ja" "en" "de" "fr" "es" "zh-cn" "ko")

# Languages that have image directories
LANGUAGES_WITH_IMAGES=("ja" "en")

# Script directory (where the script is located)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# =============================================================================
# Helper Functions
# =============================================================================

# Print colored output
print_info() {
    echo "[INFO] $1"
}

print_success() {
    echo "[SUCCESS] $1"
}

print_warning() {
    echo "[WARNING] $1"
}

print_error() {
    echo "[ERROR] $1" >&2
}

# Detect OS and return appropriate sed in-place flag
get_sed_inplace_flag() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS requires empty string after -i
        echo "-i ''"
    else
        # Linux sed
        echo "-i"
    fi
}

# Run sed with proper in-place flag based on OS
run_sed_inplace() {
    local pattern="$1"
    local file="$2"

    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "$pattern" "$file"
    else
        # Linux
        sed -i "$pattern" "$file"
    fi
}

# Find the latest version with a given major number
# Arguments: $1 = major version number, $2 = search directory
find_latest_minor_version() {
    local major="$1"
    local search_dir="$2"
    local latest_minor=-1

    # Find all directories matching the major version pattern
    for dir in "$search_dir"/"$major".*; do
        if [[ -d "$dir" ]]; then
            # Extract the minor version number
            local version=$(basename "$dir")
            local minor=${version#$major.}

            # Check if minor is a valid number
            if [[ "$minor" =~ ^[0-9]+$ ]] && [[ "$minor" -gt "$latest_minor" ]]; then
                latest_minor=$minor
            fi
        fi
    done

    if [[ "$latest_minor" -ge 0 ]]; then
        echo "$major.$latest_minor"
    else
        echo ""
    fi
}

# Calculate the previous version
# Arguments: $1 = new version (e.g., "15.4" or "16.0")
calculate_previous_version() {
    local new_version="$1"
    local major="${new_version%%.*}"
    local minor="${new_version#*.}"

    if [[ "$minor" -gt 0 ]]; then
        # Simple case: decrement minor version
        echo "$major.$((minor - 1))"
    else
        # Minor is 0, need to find the latest version of previous major
        local prev_major=$((major - 1))
        local latest=$(find_latest_minor_version "$prev_major" "$SCRIPT_DIR/ja")

        if [[ -z "$latest" ]]; then
            print_error "Could not find any version for major version $prev_major"
            exit 1
        fi

        echo "$latest"
    fi
}

# Validate version format (X.Y where X and Y are numbers)
validate_version_format() {
    local version="$1"
    if [[ ! "$version" =~ ^[0-9]+\.[0-9]+$ ]]; then
        print_error "Invalid version format: $version"
        print_error "Version must be in format X.Y (e.g., 15.4)"
        exit 1
    fi
}

# =============================================================================
# Main Script
# =============================================================================

# Check command line arguments
if [[ $# -lt 1 ]]; then
    print_error "Usage: $0 <new_version>"
    print_error "Example: $0 15.4"
    exit 1
fi

NEW_VERSION="$1"

# Validate version format
validate_version_format "$NEW_VERSION"

# Calculate previous version
PREV_VERSION=$(calculate_previous_version "$NEW_VERSION")
print_info "New version: $NEW_VERSION"
print_info "Previous version: $PREV_VERSION"

# =============================================================================
# Pre-flight Checks
# =============================================================================

print_info "Running pre-flight checks..."

# Check if any new version directory already exists
errors_found=0

for lang in "${LANGUAGES[@]}"; do
    new_dir="$SCRIPT_DIR/$lang/$NEW_VERSION"
    if [[ -d "$new_dir" ]]; then
        print_error "Directory already exists: $new_dir"
        errors_found=1
    fi
done

for lang in "${LANGUAGES_WITH_IMAGES[@]}"; do
    new_img_dir="$SCRIPT_DIR/resources/images/$lang/$NEW_VERSION"
    if [[ -d "$new_img_dir" ]]; then
        print_error "Image directory already exists: $new_img_dir"
        errors_found=1
    fi
done

if [[ $errors_found -eq 1 ]]; then
    print_error "Pre-flight check failed. Please remove existing directories first."
    exit 1
fi

print_success "Pre-flight checks passed"

# =============================================================================
# Process Documentation Directories
# =============================================================================

print_info "Processing documentation directories..."

processed_langs=()
skipped_langs=()

for lang in "${LANGUAGES[@]}"; do
    prev_dir="$SCRIPT_DIR/$lang/$PREV_VERSION"
    new_dir="$SCRIPT_DIR/$lang/$NEW_VERSION"

    if [[ ! -d "$prev_dir" ]]; then
        print_warning "Skipping $lang: Previous version directory not found: $prev_dir"
        skipped_langs+=("$lang")
        continue
    fi

    # Copy directory
    print_info "Copying $prev_dir to $new_dir"
    cp -r "$prev_dir" "$new_dir"

    # Replace version numbers in RST files
    print_info "Replacing version numbers in $new_dir/*.rst files"
    find "$new_dir" -name "*.rst" -type f | while read -r rst_file; do
        run_sed_inplace "s/$PREV_VERSION/$NEW_VERSION/g" "$rst_file"
    done

    processed_langs+=("$lang")
    print_success "Processed: $lang"
done

# =============================================================================
# Process Image Directories
# =============================================================================

print_info "Processing image directories..."

processed_img_langs=()
skipped_img_langs=()

for lang in "${LANGUAGES_WITH_IMAGES[@]}"; do
    prev_img_dir="$SCRIPT_DIR/resources/images/$lang/$PREV_VERSION"
    new_img_dir="$SCRIPT_DIR/resources/images/$lang/$NEW_VERSION"

    if [[ ! -d "$prev_img_dir" ]]; then
        print_warning "Skipping images for $lang: Previous version directory not found: $prev_img_dir"
        skipped_img_langs+=("$lang")
        continue
    fi

    # Copy image directory
    print_info "Copying $prev_img_dir to $new_img_dir"
    cp -r "$prev_img_dir" "$new_img_dir"

    processed_img_langs+=("$lang")
    print_success "Processed images: $lang"
done

# =============================================================================
# Summary
# =============================================================================

echo ""
echo "=============================================="
echo "Summary"
echo "=============================================="
echo "New version: $NEW_VERSION"
echo "Previous version: $PREV_VERSION"
echo ""
echo "Documentation directories:"
echo "  Processed: ${processed_langs[*]:-none}"
echo "  Skipped: ${skipped_langs[*]:-none}"
echo ""
echo "Image directories:"
echo "  Processed: ${processed_img_langs[*]:-none}"
echo "  Skipped: ${skipped_img_langs[*]:-none}"
echo "=============================================="

print_success "Version $NEW_VERSION created successfully!"
