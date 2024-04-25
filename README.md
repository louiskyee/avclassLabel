# AVClass Labeling Tool

## Introduction
The AVClass Labeling Tool is a Python script that allows users to classify malware families from reports obtained from VirusTotal using the [AVClass]((https://github.com/malicialab/avclass.git)) tool.

## Prerequisites
* python >= 3.10
* package
  ```cmd=
  pip3 install tqdm
  pip3 install avclass-malicialab
  ```

## Useage
```python=
python3 avclass_label.py --input_folder <input_folder>
```
### parameter
* `--input_folder` or `-i`: The folder path that stores the VirusTotal JSON report files. This parameter is required.

### Output
* `label.csv`: This file will be generated in the same directory as the input folder. It contains the labeled malware families for each file in the input folder.

### Example
```python=
python3 avclass_label.py --input_folder ./reports/
```
In this example, the script will process all the JSON report files in the `./reports/` folder, classify the malware families using AVClass, and generate a `label.csv` file in the `./reports/` folder.

The `label.csv` file will have the following format:
```
fileName,label
file1,malwareFamily1
file2,malwareFamily2
...
```
Note: The script will automatically convert the JSON report files to a single line format before processing them with AVClass. The original JSON files will not be modified.

## License
This project is licensed under the MIT License.

## Acknowledgments
AVClass - A malware labeling tool based on VirusTotal reports.