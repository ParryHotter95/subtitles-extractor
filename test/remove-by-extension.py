import logging
import os
import sys

# if --verbose argument is passed, set logging level to DEBUG
if "--verbose" in sys.argv:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

# if -y argument is passed, set DO_NOT_PROMPT to True
DO_NOT_PROMPT = "-y" in sys.argv

# get path passed as argument, default to current directory
path = sys.argv[1] if len(sys.argv) > 1 else None
if path is None:
    logging.warning("no path provided, using current directory: %s\n", os.getcwd())
    path = os.getcwd()
# check if path is valid
if not os.path.isdir(path):
    logging.error("path is not a directory: %s\n", path)
    sys.exit(1)
# check if path is a valid directory
if not os.access(path, os.R_OK | os.X_OK):
    logging.error("path is not accessible: %s\n", path)
    sys.exit(1)

logging.debug("path to clean: %s\n", path)

# get filetypes to delete
filetypes_to_delete = []
if len(sys.argv) > 2:
    for filetype in sys.argv[2:]:
        # check if filetype contains any
        if filetype.startswith('.'):
            filetypes_to_delete.append(filetype)
        else:
            filetypes_to_delete.append('.' + filetype)
else:
    logging.error("no filetypes provided\n")
    sys.exit(1)

logging.debug("filetypes to delete: %s\n", filetypes_to_delete)

files = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
logging.debug("files: %s\n", files)

files_to_delete = [file for file in files if os.path.splitext(file)[1] in filetypes_to_delete]
print("\nfollowing files will be deleted:")
for file in files_to_delete:
    print(file)
# ask user if to proceed
proceed = input("Proceed? (y/n): ")

if proceed.lower() != 'y':
    sys.exit(0)
else:
    counter = 0
    for file in files_to_delete:
        try:
            os.remove(os.path.join(path, file))
            counter += 1
        except OSError:
            print("Error while deleting file: " + file)
        logging.debug("deleted %s\n", file)
    logging.info("number of files deleted: %d\n", counter)
    sys.exit(0)