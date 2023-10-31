# avclassLabel

## Introduction
The primary function is to allow users to use [avclass](https://github.com/malicialab/avclass.git) to classify malware families from reports obtained from VirusTotal.

## Prerequisites
* python >= 3.10
* package
  ```cmd=
  pip3 install tqdm
  pip3 install avclass-malicialab
  ```

## Useage
```python=
python3 avclassLabel.py -i <inputFolder> -o <outputPath> -c <convertToOneLine>
```
### parameter
* `-i`: (`--input-folder`)
  * inputFolder: The folder path that stores VirusTotal reports.
* `-o`: (`--output-path`)
  * outputPath: Set the file location to output label.csv.
* `-c`: (`--convert-to-one-line`)
  * convertToOneLine: Confirm whether you want to change the json file into one line. (True or False)

### Output
* `label.csv`: This file stores the labeled malware families.

### Example
```python=
python3 avclassLabel.py -i ./report/ -o ./label.csv -c False
```
