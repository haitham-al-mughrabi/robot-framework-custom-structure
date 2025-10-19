#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

REQUIREMENTS_FILE="requirements.txt"
DOCKER_SCRIPT="./prepare_docker.sh"

# Default behavior - rebuild by default
REBUILD=true

# Function to print colored output
print_colored() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 <action> [package] [version] [options]"
    echo ""
    echo "Actions:"
    echo "  install <package> [version]  - Install a package (latest if no version specified)"
    echo "  update <package> [version]   - Update an existing package"
    echo "  delete <package>             - Remove a package from requirements"
    echo "  list                         - List all packages in requirements.txt"
    echo "  rebuild                      - Rebuild Docker image without package changes"
    echo ""
    echo "Options:"
    echo "  --no-rebuild, -n             - Skip Docker image rebuild (default: rebuild)"
    echo "  --help, -h                   - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 install selenium"
    echo "  $0 install requests 2.28.1 --no-rebuild"
    echo "  $0 update robotframework 6.1.1 -n"
    echo "  $0 delete pytest --no-rebuild"
    echo "  $0 list"
    echo ""
}

# Function to parse command line arguments
parse_arguments() {
    local args=("$@")
    local non_flag_args=()
    
    # Parse all arguments
    for ((i=0; i<${#args[@]}; i++)); do
        case "${args[i]}" in
            --no-rebuild|-n)
                REBUILD=false
                ;;
            --help|-h)
                show_usage
                exit 0
                ;;
            -*)
                print_colored $RED "Error: Unknown option '${args[i]}'"
                show_usage
                exit 1
                ;;
            *)
                non_flag_args+=("${args[i]}")
                ;;
        esac
    done
    
    # Return non-flag arguments
    printf '%s\n' "${non_flag_args[@]}"
}

# Function to create requirements.txt if it doesn't exist
ensure_requirements_file() {
    if [[ ! -f "$REQUIREMENTS_FILE" ]]; then
        print_colored $YELLOW "Creating $REQUIREMENTS_FILE..."
        cat > "$REQUIREMENTS_FILE" << EOF
# Robot Framework and common dependencies
robotframework>=6.0.0
selenium>=4.0.0
robotframework-seleniumlibrary>=6.0.0

# Add your additional Python dependencies here
# Example:
# requests>=2.28.0
# pytest>=7.0.0
EOF
        print_colored $GREEN "$REQUIREMENTS_FILE created with default Robot Framework dependencies"
    fi
}

# Function to check if package exists in requirements.txt
package_exists_in_requirements() {
    local package=$1
    if [[ -f "$REQUIREMENTS_FILE" ]]; then
        # Check for package name (case-insensitive, handle various formats)
        grep -i "^${package}[>=<~!]" "$REQUIREMENTS_FILE" > /dev/null 2>&1 || \
        grep -i "^${package}$" "$REQUIREMENTS_FILE" > /dev/null 2>&1
    else
        return 1
    fi
}

# Function to get current package version from requirements.txt
get_package_version_from_requirements() {
    local package=$1
    if package_exists_in_requirements "$package"; then
        grep -i "^${package}" "$REQUIREMENTS_FILE" | head -1 | sed 's/.*[>=<~!]\+//' || echo "latest"
    else
        echo ""
    fi
}

# Function to remove package from requirements.txt
remove_package_from_requirements() {
    local package=$1
    if [[ -f "$REQUIREMENTS_FILE" ]]; then
        # Create temporary file and remove lines matching the package
        grep -v -i "^${package}[>=<~!]" "$REQUIREMENTS_FILE" > "${REQUIREMENTS_FILE}.tmp" || true
        grep -v -i "^${package}$" "${REQUIREMENTS_FILE}.tmp" > "${REQUIREMENTS_FILE}" || true
        rm -f "${REQUIREMENTS_FILE}.tmp"
    fi
}

# Function to add package to requirements.txt
add_package_to_requirements() {
    local package=$1
    local version=$2
    
    ensure_requirements_file
    
    if [[ -n "$version" ]]; then
        echo "${package}==${version}" >> "$REQUIREMENTS_FILE"
    else
        echo "$package" >> "$REQUIREMENTS_FILE"
    fi
}

# Function to rebuild Docker image
rebuild_docker() {
    if [[ "$REBUILD" == true ]]; then
        print_colored $BLUE "Rebuilding Docker image..."
        if [[ -x "$DOCKER_SCRIPT" ]]; then
            $DOCKER_SCRIPT
            print_colored $GREEN "Docker image rebuilt successfully!"
        else
            print_colored $RED "Error: $DOCKER_SCRIPT not found or not executable"
            exit 1
        fi
    else
        print_colored $YELLOW "Skipping Docker rebuild (--no-rebuild flag specified)"
        print_colored $BLUE "Remember to run '$DOCKER_SCRIPT' or '$0 rebuild' when ready to update the image"
    fi
}

# Function to install package
install_package() {
    local package=$1
    local version=$2
    
    ensure_requirements_file
    
    if package_exists_in_requirements "$package"; then
        local current_version=$(get_package_version_from_requirements "$package")
        print_colored $YELLOW "Package '$package' is already installed"
        if [[ -n "$current_version" && "$current_version" != "latest" ]]; then
            print_colored $YELLOW "Current version: $current_version"
        fi
        
        read -p "Do you want to update it instead? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            update_package "$package" "$version"
        else
            print_colored $BLUE "No changes made."
        fi
    else
        print_colored $GREEN "Adding '$package' to requirements.txt..."
        add_package_to_requirements "$package" "$version"
        
        if [[ -n "$version" ]]; then
            print_colored $GREEN "Added $package==$version to requirements.txt"
        else
            print_colored $GREEN "Added $package (latest) to requirements.txt"
        fi
        
        rebuild_docker
    fi
}

# Function to update package
update_package() {
    local package=$1
    local version=$2
    
    ensure_requirements_file
    
    if package_exists_in_requirements "$package"; then
        local current_version=$(get_package_version_from_requirements "$package")
        print_colored $YELLOW "Updating '$package'..."
        if [[ -n "$current_version" && "$current_version" != "latest" ]]; then
            print_colored $YELLOW "Current version: $current_version"
        fi
        
        # Remove old entry and add new one
        remove_package_from_requirements "$package"
        add_package_to_requirements "$package" "$version"
        
        if [[ -n "$version" ]]; then
            print_colored $GREEN "Updated $package to version $version"
        else
            print_colored $GREEN "Updated $package to latest version"
        fi
        
        rebuild_docker
    else
        print_colored $RED "Package '$package' not found in requirements.txt"
        read -p "Do you want to install it instead? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            install_package "$package" "$version"
        fi
    fi
}

# Function to delete package
delete_package() {
    local package=$1
    
    if package_exists_in_requirements "$package"; then
        print_colored $YELLOW "Removing '$package' from requirements.txt..."
        remove_package_from_requirements "$package"
        print_colored $GREEN "Removed $package from requirements.txt"
        rebuild_docker
    else
        print_colored $RED "Package '$package' not found in requirements.txt"
    fi
}

# Function to list packages
list_packages() {
    ensure_requirements_file
    
    print_colored $BLUE "Packages in $REQUIREMENTS_FILE:"
    echo "=================================="
    
    if [[ -f "$REQUIREMENTS_FILE" ]]; then
        # Filter out comments and empty lines, then format nicely
        grep -v '^#' "$REQUIREMENTS_FILE" | grep -v '^$' | while read -r line; do
            if [[ -n "$line" ]]; then
                echo "  • $line"
            fi
        done
    else
        print_colored $YELLOW "No requirements.txt file found"
    fi
    echo "=================================="
}

# Function to force rebuild
force_rebuild() {
    print_colored $BLUE "Force rebuilding Docker image..."
    if [[ -x "$DOCKER_SCRIPT" ]]; then
        $DOCKER_SCRIPT
        print_colored $GREEN "Docker image rebuilt successfully!"
    else
        print_colored $RED "Error: $DOCKER_SCRIPT not found or not executable"
        exit 1
    fi
}

# Main script logic
main() {
    if [[ $# -eq 0 ]]; then
        show_usage
        exit 1
    fi
    
    # Parse arguments and get non-flag arguments
    local non_flag_args
    mapfile -t non_flag_args < <(parse_arguments "$@")
    
    local action="${non_flag_args[0]}"
    local package="${non_flag_args[1]}"
    local version="${non_flag_args[2]}"
    
    case "$action" in
        "install")
            if [[ -z "$package" ]]; then
                print_colored $RED "Error: Package name required for install action"
                show_usage
                exit 1
            fi
            install_package "$package" "$version"
            ;;
        "update")
            if [[ -z "$package" ]]; then
                print_colored $RED "Error: Package name required for update action"
                show_usage
                exit 1
            fi
            update_package "$package" "$version"
            ;;
        "delete"|"remove")
            if [[ -z "$package" ]]; then
                print_colored $RED "Error: Package name required for delete action"
                show_usage
                exit 1
            fi
            delete_package "$package"
            ;;
        "list"|"ls")
            list_packages
            ;;
        "rebuild")
            force_rebuild
            ;;
        *)
            print_colored $RED "Error: Unknown action '$action'"
            show_usage
            exit 1
            ;;
    esac
}

# Check if prepare_docker.sh exists
if [[ ! -f "$DOCKER_SCRIPT" ]]; then
    print_colored $RED "Warning: $DOCKER_SCRIPT not found in current directory"
    print_colored $YELLOW "Make sure you're running this script from the same directory as $DOCKER_SCRIPT"
fi

# Run main function with all arguments
main "$@"
