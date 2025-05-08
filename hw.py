import ctypes

# Load the COBOL shared library
lib = ctypes.CDLL("./hw.dylib")

lib.cob_init()


# Call the main function (if defined)
lib.IDSAMPLE()


lib.cob_stop_run()

