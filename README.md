# Broadband Geopackage Project

This project is designed to organize US FCC BDC reported broad band serice location files for each US state and territory, ready for
further processing with catfccbdc.

## Project Structure

```
fccbdcln
├── src
│   ├── constant.py        # Contains constants for the project
│   └── main.py            # Main entry point for the project
├── data
│   ├── USA_FCC-bdc        # Directory for FCC bdc service locations files
├── requirements.txt       # Lists project dependencies
├── setup.py               # Packaging and metadata for the project
└── README.md              # Project documentation
```

## Usage

### Command Line Arguments

- `--base-dir`: Specifies the base directory for processing. Defaults to the current working directory.
- `--log-file`: Specifies the log file path. If this argument is provided, logging will be enabled and logs will be written to the specified log file.
- `-s` or `--state`: Specifies the state abbreviation(s) to process. This argument accepts one or more state abbreviations.

### Example Commands

To run the script with the `--base-dir` argument, enable logging, and process specific states:

```sh
python main.py --base-dir /path/to/base-dir --log-file my_log.log --state OR WA

## Requirements

Ensure you have the necessary dependencies installed by running:

```
pip install -r requirements.txt
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
