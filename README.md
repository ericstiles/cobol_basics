This repository, created by a very new user (me :-) still learning), contains a simple example of how to call a COBOL program from Python using GnuCOBOL on MacOS.

# Steps
## Prework

Install Homebrew, set path and verify.

```
$ brew install gnucobol
$ echo 'export PATH=$PATH:/usr/local/Cellar/gnucobol/3.2/bin' >> ~/.zshrc
$ source ~/.zshrc
$ cobc --version

cobc (GnuCOBOL) 3.2.0
Copyright (C) 2023 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
Written by Keisuke Nishida, Roger While, Ron Norman, Simon Sobisch, Edward Hart
Built     Jul 28 2023 18:42:18
Packaged  Jul 28 2023 17:02:56 UTC
C version "Apple LLVM 15.0.0 (clang-1500.0.40.1)" 
```

Additional step that sets a path for the library to be found by the linker. Unsure if this is needed. 
[https://stackoverflow.com/questions/1231950/how-to-set-dyld_library_path-in-mac-os-x]

```
export DYLD_LIBRARY_PATH=./:$DYLD_LIBRARY_PATH
```

## Simple Cobol Program

Create file: `hw.pgm` with the following content.

```
IDENTIFICATION DIVISION.
PROGRAM-ID. IDSAMPLE.
ENVIRONMENT DIVISION.
PROCEDURE DIVISION.
    DISPLAY 'HELLO WORLD'.
    STOP RUN.
```

Run the following commands in the terminal to compile:

```
$ cobc -x -o hw.dylib hw.pgm
```

Run the following commands in the terminal to see information.

```
$ nm -gU hw.dylib
00000000000006d0 T _IDSAMPLE
```

See more information. Otool is a command line tool for displaying information about Mach-O files.

```
$ otool -L hw.dylib

hw.dylib:
	/usr/local/opt/gnucobol/lib/libcob.4.dylib (compatibility version 7.0.0, current version 7.0.0)
	/usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 1351.0.0)

```

## Python

Create file: `hw.py` with the following content.

```python
import ctypes

# Load the COBOL shared library
lib = ctypes.CDLL("./hw.dylib")

lib.cob_init()

# Call the main function (if defined)
lib.IDSAMPLE()

lib.cob_stop_run()
```

Run the following commands in the terminal to see information.

```
$ python3 hw.py
HELLO WORLD
```

# More Examples In Other Branches
- [data_items in 1_data_items folder](https://github.com/ericstiles/cobol_basics/tree/data_items/1_data_items)