"""
File Reader and Modifier
A program that reads a file, applies modifications, and writes to a new file.
"""

import os
import sys


def modify_text(content):
    """
    This function converts file contents to uppercase and adds line numbers.
    """
    lines = content.splitlines()
    modified_lines = []

    for i, line in enumerate(lines, 1):
        modified_line = f"{i:3d}: {line.upper()}"
        modified_lines.append(modified_line)

    return '\n'.join(modified_lines)


def get_output_filename(input_filename):
    """Generate output filename based on input filename."""
    name, ext = os.path.splitext(input_filename)
    return f"{name}_modified{ext}"


def read_and_modify_file():
    """Main function to handle file reading and modification."""

    while True:
        # Get filename from user
        filename = input("Enter the filename to read: ").strip()

        if not filename:
            print("Please enter a valid filename.")
            continue

        try:
            # Check if file exists
            if not os.path.exists(filename):
                print(f"Error: File '{filename}' does not exist.")
                retry = input(
                    "Would you like to try another filename? (y/n): ").lower()
                if retry != 'y':
                    return
                continue

            # Check if it's actually a file (not a directory)
            if not os.path.isfile(filename):
                print(f"Error: '{filename}' is not a regular file.")
                retry = input(
                    "Would you like to try another filename? (y/n): ").lower()
                if retry != 'y':
                    return
                continue

            # Try to read the file
            print(f"Reading file '{filename}'...")
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()

            print(
                f"Successfully read {len(content)} characters from '{filename}'")

            # Modify the content
            print("Modifying content...")
            modified_content = modify_text(content)

            # Generate output filename
            output_filename = get_output_filename(filename)

            # Ask user if they want to use the default output name or specify their own
            user_output = input(
                f"Output filename (press Enter for '{output_filename}'): ").strip()
            if user_output:
                output_filename = user_output

            # Write modified content to new file
            try:
                with open(output_filename, 'w', encoding='utf-8') as output_file:
                    output_file.write(modified_content)

                print(
                    f"Successfully wrote modified content to '{output_filename}'")
                print(f"Original file: {len(content.splitlines())} lines")
                print(
                    f"Modified file: {len(modified_content.splitlines())} lines")

                # Ask if user wants to see a preview
                preview = input(
                    "Would you like to see a preview of the modified content? (y/n): ").lower()
                if preview == 'y':
                    lines = modified_content.splitlines()
                    preview_lines = min(10, len(lines))
                    print(f"\nFirst {preview_lines} lines of modified content:")
                    print("-" * 50)
                    for line in lines[:preview_lines]:
                        print(line)
                    if len(lines) > preview_lines:
                        print(f"... and {len(lines) - preview_lines} more lines")
                    print("-" * 50)

                break

            except PermissionError:
                print(f"Error: Permission denied when writing to '{output_filename}'")
                print("Make sure you have write permissions to this location.")
                return
            except OSError as e:
                print(f"Error writing to file '{output_filename}': {e}")
                return

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except PermissionError:
            print(f"Error: Permission denied when reading '{filename}'")
            print("Make sure you have read permissions for this file.")
        except UnicodeDecodeError:
            print(f"Error: Unable to decode '{filename}' as UTF-8 text.")
            print("The file might be a binary file or use a different encoding.")
        except OSError as e:
            print(f"Error reading file '{filename}': {e}")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            return
        except Exception as e:
            print(f"Unexpected error: {e}")

        # Ask if user wants to try again
        retry = input(
            "Would you like to try another filename? (y/n): ").lower()
        if retry != 'y':
            return


def main():
    """Main program entry point."""
    print("File Reader and Modifier")
    print("=" * 30)
    print("This program reads a text file, modifies it (adds line numbers and converts to uppercase),")
    print("and saves the result to a new file.")
    print()

    try:
        read_and_modify_file()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Goodbye!")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

    print("Thank you for using File Reader and Modifier!")


if __name__ == "__main__":
    main()
