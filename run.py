from FileConverter import FileConverter

try:
    fc = FileConverter()
    fc.start()
except Exception as e:
    print(e)
