import os
import sys
import json
import time
import argparse
import subprocess

from tqdm import tqdm
from multiprocessing import Pool

DEFAULT_INPUT_PATH = ""
DEFAULT_OUTPUT_PATH = ""
DEFAULT_CONVERT_FLAG = False

class avclass(object):
    def __init__(self):
        '''
        Initialize default values for various parameters
        '''
        self.datasetPath = DEFAULT_INPUT_PATH  # Default input dataset folder path
        self.outputPath = DEFAULT_OUTPUT_PATH
        self.fileList = list() # List to store file paths
        self.convertFlag = DEFAULT_CONVERT_FLAG

    def run(self):
        if 'ipykernel' not in sys.modules:
            self.parameter_parser()
        self.get_all_files_in_directory()
        if self.convertFlag:
            self.convert_to_one_line()
        # self.avclass_label()

    def parameter_parser(self):
        '''
        A method for parsing command line parameters
        using `python argparse`.
        '''
        parser = argparse.ArgumentParser(description="Parse command line parameters.")
    
        parser.add_argument("--input-folder", "-i",
                            dest="input_folder",
                            nargs="?",
                            default=DEFAULT_INPUT_PATH,
                            help="Input dataset folder."
                            )
        parser.add_argument("--output-path", "-o",
                            dest="output_path",
                            nargs="?",
                            default=DEFAULT_OUTPUT_PATH,
                            help="Output label.csv"
                            )
        parser.add_argument("--convert-to-one-line", "-c",
                            dest="convertFlag",
                            nargs="?",
                            default=DEFAULT_CONVERT_FLAG,
                            help="Confirm whether you want to change the json file into one line."
                            )
        args = parser.parse_args()
    
        # Save the 'args' parameter in the 'avclass' class
        self.datasetPath = args.input_folder
        self.outputPath = args.output_path
        self.convertFlag = args.convertFlag
        
    def get_all_files_in_directory(self):
        '''
        Get a list of all files in the folder and its subfolders
        '''
        allFiles = list(os.walk(self.datasetPath))
        for root, dirs, files in tqdm(allFiles, desc="Get all files"):
            for file in files:
                file_path = os.path.join(root, file)
                self.fileList.append(file_path)

    def convert_to_one_line(self):
        for path in tqdm(self.fileList, desc="convert to one line"):
            with open(path, encoding="utf-8") as f:
                data = json.load(f)           

                with open(path, "w") as f:
                    json.dump(data, f, separators=(',', ':'))

    def process_json(self, json_file):
        fileName = os.path.basename(json_file)[:-5]
        command = f"avclass -f {json_file}"
        try:
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
            if result.returncode == 0:
                label = (result.stdout).split()[1]
            else:
                print(f"Command execution failed ({json_file}), error message:")
                print(result.stderr)
                label = "Error"
        except subprocess.CalledProcessError as e:
            print(f"Command execution error ({json_file}), error message:")
            print(e.stderr)
            label = "Error"
        except Exception as e:
            print(f"An error occurred ({json_file}):", str(e))
            label = "Error"
    
        return fileName, label
    
    def avclass_label(self):
        start_time = time.time()  # Record start time
        with open(self.outputPath, encoding="utf-8", mode='w') as f:
            f.write(f"fileName,label\n")
            
        # Process JSON files serially
            for fileName in tqdm(self.fileList, desc="Label malware"):
                fileName, label = self.process_json(fileName)
                f.write(f"{fileName},{label}\n")
    
        end_time = time.time() # Record end time
        execution_time = end_time - start_time # Calculate execution time
        with open('time.txt', 'w') as time_file:
            time_file.write(f"Execution Time: {execution_time} seconds")

def process_json(json_file):
    fileName = os.path.basename(json_file)[:-5]
    command = f"avclass -f {json_file}"
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        if result.returncode == 0:
            label = (result.stdout).split()[1]
        else:
            print(f"Command execution failed ({json_file}), error message:")
            print(result.stderr)
            label = "Error"
    except subprocess.CalledProcessError as e:
        print(f"Command execution error ({json_file}), error message:")
        print(e.stderr)
        label = "Error"
    except Exception as e:
        print(f"An error occurred ({json_file}):", str(e))
        label = "Error"

    return fileName, label
    
if __name__ == "__main__":
    avLabel = avclass()
    avLabel.run()
    
    start_time = time.time()  # Record start time
    with open(avLabel.outputPath, encoding="utf-8", mode='w') as f:
        f.write(f"fileName,label\n")
        
        # Use 8 processes to handle JSON files
        with Pool(8) as pool:
            for fileName, label in tqdm(pool.imap(process_json, avLabel.fileList), total=len(avLabel.fileList), desc="Label malware"):
                f.write(f"{fileName},{label}\n")
                
    end_time = time.time() # Record end time
    execution_time = end_time - start_time # Calculate execution time
    with open('time.txt', 'w') as time_file:
        time_file.write(f"Execution Time: {execution_time} seconds")