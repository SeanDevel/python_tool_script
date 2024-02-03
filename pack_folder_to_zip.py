import datetime, os, sys, zipfile, getopt
"""
Pack a folder into a zip file with a given subject name for backup archives.

Args:
    archive_path (str): The path to the folder to be zipped.
    subject_name (str): The name of the subject for the backup.

Returns:
    str: The name of the created zip archive, or None if an error occurred.
"""


def pack_folder_to_zip(archive_path: str, subject_name: str):
    if not os.path.exists(archive_path):
        print(f"No such directory: {archive_path}")
        return None
    if not os.path.isdir(archive_path):
        print(f"Not a directory: {archive_path}")
        return None
    now = datetime.datetime.now()
    date_format = now.strftime("%y-%m-%d_%H.%M.%S")
    archive_name = f"backup_{subject_name}@{date_format}.zip"

    try:
        with zipfile.ZipFile(archive_name, "w",
                             zipfile.ZIP_DEFLATED) as zip_file:
            for root, _, files in os.walk(archive_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, archive_path)
                    zip_file.write(file_path, arcname)
        return archive_name
    except Exception as e:
        print(f"Error creating zip archive: {e}")
        return None


"""
Function to check the packing status of an archive
depends on the argument passed is None or not

Args:
    archive_name (str): The name of the archive to check.

Returns:
    str: A message indicating the packing status of the archive.
"""


def packing_status(archive_name):
    if archive_name:
        return f"Folder packed successfully: {archive_name}"
    else:
        return "Failed to create archive."


def print_usage():
    print("Usage: python ./script.py -p <path> -n <name>")
    print("Options:")
    print("-p, --path: The path to the archive directory")
    print("-n, --name: The name of the backup")


if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:n:", ["path=", "name="])
    except getopt.GetoptError as err:
        print(err)
        print_usage()
        sys.exit(2)
    archive_path = None
    subject_name = None
    for opt, arg in opts:
        if opt in ('-p', '--path'):
            archive_path = arg
        if opt in ['-n', '--name']:
            subject_name = arg
    if not archive_path or not subject_name:
        print("Missing required arguments.")
        print_usage()
        sys.exit(2)
    packed_zip_path = pack_folder_to_zip(archive_path, subject_name)
    print(packing_status(packed_zip_path))
