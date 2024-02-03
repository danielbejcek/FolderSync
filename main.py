import os
import shutil
import logging
import argparse
import time

currentDir = os.path.dirname(__file__)

"""Paths to designated directories"""
sourceDir_path = os.path.join(currentDir,"Task folders","Source")
replicaDir_path = os.path.join(currentDir,"Task folders","Replica")

"""Creates a separate logging file that keeps track of all folder changes"""
logging.basicConfig(filename="foldersync_log.log",
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    filemode='w')

"""Parser that provides specific arguments, which are then passed into a command line"""
parser = argparse.ArgumentParser(
        prog='Veeam Task',
        description='Synchronization of two folders.')
parser.add_argument("interval",type=int,help="Time between each synchronization.")
parser.add_argument("sync_logFile")
args = parser.parse_args()


def syncFolders():
    """Main folders that are being updated after each given interval"""
    sourceDir = os.listdir(os.path.join(sourceDir_path))
    replicaDir = os.listdir(os.path.join(replicaDir_path))

    for item in sourceDir:
        """Destination folder path"""
        replicaFolder = os.path.join(replicaDir_path, item)

        """Check to verify if an item within the 'sourceDir' is a directory"""
        if os.path.isdir(os.path.join(sourceDir_path,item)):
            sourceFolder = os.path.join(sourceDir_path,item)
            if sourceFolder not in replicaDir:
                try:
                    shutil.copytree(sourceFolder,replicaFolder)
                    logging.info(f"Directory: '{item}' was successfully copied into '{replicaDir_path}'")
                    print(f"Directory: '{item}' was successfully copied into '{replicaDir_path}'")
                except FileExistsError:
                    """To maintain each directory updated, folder is removed and added again each iteration"""
                    shutil.rmtree(replicaFolder)
                    shutil.copytree(sourceFolder,replicaFolder)

        """Check to verify if an item within the 'sourceDir' is a file"""
        if os.path.isfile(os.path.join(sourceDir_path,item)):
            sourceFile = os.path.join(sourceDir_path,item)
            if not os.path.exists(replicaFolder):
                shutil.copy2(sourceFile,replicaFolder)
                logging.info(f"File: '{item}' was successfully copied into: '{replicaDir_path}'")
                print(f"File: '{item}' was successfully copied into: '{replicaDir_path}'")
            else:
                """Overwrite a file in case it already exists with 'copy2' method to keep it updated"""
                shutil.copy2(sourceFile,replicaFolder)


        """Update the 'replicaDir' by verifying what items are in the 'sourceDir' and removing them afterwards"""
        for itemCopy in replicaDir:
            if os.path.isdir(os.path.join(replicaDir_path,itemCopy)) and itemCopy not in sourceDir:
                    try:
                        shutil.rmtree(os.path.join(replicaDir_path, itemCopy))
                        logging.info(f"Directory: '{itemCopy}' was successfully removed from '{replicaDir_path}'")
                        print(f"Directory: '{itemCopy}' was successfully removed from '{replicaDir_path}'")
                    except FileNotFoundError:
                        pass

            if os.path.isfile(os.path.join(replicaDir_path,itemCopy)) and itemCopy not in sourceDir:
                    try:
                        os.remove(os.path.join(replicaDir_path, itemCopy))
                        logging.info(f"File: '{itemCopy}' was successfully removed from '{replicaDir_path}'")
                        print(f"File: '{itemCopy}' was successfully removed from '{replicaDir_path}'")
                    except FileNotFoundError:
                        pass

def main():
    while True:
        logging.info("Starting folder synchronization.\n")
        syncFolders()
        logging.info("Folder synchronization finished.\n")
        time.sleep(args.interval)

if __name__ == "__main__":
    main()



