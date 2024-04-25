import os
import sys
import json
import time
import argparse
import subprocess

from tqdm import tqdm
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

class Config:
    def __init__(self, input_dir):
        """
        Initialize the configuration object.

        :param input_dir: The input directory containing the JSON files.
        """
        self.input_dir = input_dir
        self.output_path = self.get_output_path()

    def get_output_path(self):
        """
        Get the output path for the label.csv file.

        :return: The output path for the label.csv file.
        """
        return os.path.join(self.input_dir, "label.csv")

class AVClass:
    def __init__(self, config: Config):
        """
        Initialize the AVClass object.

        :param config: The configuration object containing the input directory and output path.
        """
        self.config = config
        if not os.path.isdir(config.input_dir):
            print("Error: Input path must be a directory.")
            sys.exit(1)
        self.file_list = []

    def run(self):
        """
        Run the AVClass labeling process.
        """
        self.get_all_files_in_directory()
        self.avclass_label()
        print(f"Output label.csv path: {Path(self.config.output_path).resolve()}")

    def get_all_files_in_directory(self):
        """
        Get all JSON files in the input directory and its subdirectories.
        """
        all_files = list(os.walk(self.config.input_dir))
        for root, dirs, files in tqdm(all_files, desc="Getting files", unit="dir"):
            for file in files:
                if not file.endswith(".json"):
                    continue
                file_path = os.path.join(root, file)
                self.file_list.append(file_path)

    def convert_to_one_line(self, json_file):
        """
        Convert the JSON file to a single line string.

        :param json_file: The path to the JSON file.
        :return: The single line string representation of the JSON file, or None if an error occurs.
        """
        try:
            with open(json_file, encoding="utf-8") as f:
                data = json.load(f)
            return json.dumps(data, separators=(',', ':'))
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON file ({json_file}): {str(e)}")
            return None
        except Exception as e:
            print(f"Error reading JSON file ({json_file}): {str(e)}")
            return None

    def process_json(self, json_file):
        """
        Process a single JSON file using AVClass.

        :param json_file: The path to the JSON file.
        :return: A tuple containing the file name (without extension) and the AVClass label.
        """
        file_name = os.path.basename(json_file)[:-5]
        one_line_data = self.convert_to_one_line(json_file)
        if one_line_data is None:
            print(f"Processing {json_file}")
            return file_name, "Error"
        with open(json_file + ".tmp", "w", encoding='utf-8') as tmp_file:
            tmp_file.write(one_line_data)
        command = f"avclass -f {json_file}.tmp"
        try:
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
            if result.returncode == 0:
                label = result.stdout.split()[1]
            else:
                print(f"Command execution failed ({json_file})")
                label = "Error"
        except subprocess.CalledProcessError as e:
            print(f"Command execution error ({json_file})")
            label = "Error"
        except Exception as e:
            print(f"An error occurred ({json_file}): {str(e)}")
            label = "Error"
        finally:
            os.remove(json_file + ".tmp")

        return file_name, label

    def avclass_label(self):
        """
        Perform AVClass labeling on all JSON files using multi-threading.
        """
        start_time = time.time()
        
        # Create a list to store the file names and labels
        labels = []

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.process_json, json_file) for json_file in self.file_list]
            
            for future in tqdm(as_completed(futures), total=len(futures), desc="Labeling", unit="file"):
                file_name, label = future.result()
                labels.append((file_name, label))

        # Sort the labels list based on the file name
        labels.sort(key=lambda x: x[0])

        with open(self.config.output_path, encoding="utf-8", mode='w') as f:
            f.write("fileName,label\n")
            for file_name, label in labels:
                f.write(f"{file_name},{label}\n")

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution Time: {execution_time:.2f} seconds")

def parse_arguments():
    """
    Parse command-line arguments.

    :return: The parsed arguments.
    """
    parser = argparse.ArgumentParser(description="AVClass Labeling Tool")
    parser.add_argument("--input_folder", "-i", default='', help="Input dataset report folder")
    return parser.parse_args()

def main():
    """
    The main function to run the AVClass labeling process.
    """
    args = parse_arguments()
    
    config = Config(args.input_folder)
    
    av_class = AVClass(config)
    av_class.run()

if __name__ == "__main__":
    main()