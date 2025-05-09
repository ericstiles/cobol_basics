#!/usr/bin/env python3

import ctypes
import argparse
import sys
import os.path
import subprocess

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Run COBOL program with specified library')
    parser.add_argument('library_path', help='Path to the compiled COBOL library (e.g., ./di.dylib)')
    parser.add_argument('--function', default='main', 
                      help='Name of the main function to call (default: SimpleDataItemsDemo)')
    args = parser.parse_args()

    # Check if library file exists
    if not os.path.exists(args.library_path):
        print(f"Error: Library file '{args.library_path}' not found", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Load the COBOL shared library
        lib = ctypes.CDLL(args.library_path)
        
        # Initialize COBOL runtime
        try:
            lib.cob_init()
        except AttributeError:
            print(f"Error: COBOL runtime function 'cob_init' not found in '{args.library_path}'", file=sys.stderr)
            sys.exit(1)
        
        # Call the main function from the library
        # When working with compiled libraries, symbol names might be mangled.
        # For example, a function 'foo' might appear as '_foo' in the library.
        # We'll try different variations of the function name.
        function_found = False
        function_variations = [
            args.function,           # Try the name as provided
            f"_{args.function}",     # Try with underscore prefix (common in C)
            f"{args.function}_",     # Try with underscore suffix
            f"_{args.function}_"     # Try with both prefix and suffix
        ]
        
        for func_name in function_variations:
            try:
                function_to_call = getattr(lib, func_name)
                function_to_call()
                function_found = True
                print(f"Successfully called function '{func_name}'")
                break
            except AttributeError:
                continue
                
        if not function_found:
            print(f"Error: Function '{args.function}' (or variations) not found in '{args.library_path}'", file=sys.stderr)
            
            # Try to get available symbols for better error reporting
            try:
                result = subprocess.run(['nm', args.library_path], capture_output=True, text=True)
                if result.returncode == 0:
                    symbols = [line for line in result.stdout.split('\n') if ' T ' in line]
                    if symbols:
                        print("\nAvailable exported functions in the library:", file=sys.stderr)
                        for symbol in symbols:
                            print(f"  {symbol}", file=sys.stderr)
                    else:
                        print("\nNo exported functions found in the library.", file=sys.stderr)
                else:
                    print("Available functions can be checked with: nm <library_path> | grep -i 'T _'", file=sys.stderr)
            except Exception:
                print("Available functions can be checked with: nm <library_path> | grep -i 'T _'", file=sys.stderr)
                
            sys.exit(1)
        
        # Properly terminate COBOL runtime
        try:
            lib.cob_stop_run()
        except AttributeError:
            print(f"Warning: COBOL runtime function 'cob_stop_run' not found in '{args.library_path}'", file=sys.stderr)
            
    except OSError as e:
        print(f"Error loading library '{args.library_path}': {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
