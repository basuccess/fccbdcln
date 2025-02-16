# main.py

import os
import re
import shutil
import zipfile
import logging
import argparse
from datetime import datetime
from constant import STATES_AND_TERRITORIES, BDC_FILE_PATTERN, BDC_SRC_FILE_PATTERN  # Import the list and pattern from constants.py

# Configure argument parser
parser = argparse.ArgumentParser(description='Process BDC files.')
parser.add_argument('--base-dir', type=str, default=os.getcwd(), help='Base directory for processing')
parser.add_argument('--log-file', type=str, nargs='?', const='fccbdcln_log.log', help='Log file path')
parser.add_argument('-s', '--state', type=str, nargs='+', help='State abbreviation(s) to process')
args = parser.parse_args()

# Configure logging based on the presence of the log-file argument
if args.log_file is not None:
    log_file_path = os.path.join(args.base_dir, args.log_file)
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename=log_file_path, filemode='w')
else:
    logging.basicConfig(level=logging.CRITICAL)  # Disable logging by setting a high log level

base_dir = args.base_dir
bdc_dir = os.path.join(base_dir, "USA_FCC-bdc")
downloads_dir = os.path.expanduser("~/Downloads")

logging.info(f"Base directory: {base_dir}")
logging.info(f"US FCC bdc reported service location files directory: {bdc_dir}")
logging.info(f"Downloads directory: {downloads_dir}")

def remove_existing_symlinks(state_dir):
    for item in os.listdir(state_dir):
        item_path = os.path.join(state_dir, item)
        if os.path.islink(item_path):
            logging.debug(f"Removing existing symlink: {item_path}")
            os.remove(item_path)

def move_files_from_downloads(state_dir, fips_code):
    bdc_subdir = os.path.join(state_dir, 'bdc')
    if not os.path.exists(bdc_subdir):
        logging.debug(f"Creating directory: {bdc_subdir}")
        os.makedirs(bdc_subdir)

    files_moved = False
    pattern = BDC_SRC_FILE_PATTERN.replace(r'\d{2}', fips_code, 1)
    logging.debug(f"Using pattern: {pattern}")
    for file_name in os.listdir(downloads_dir):
        logging.debug(f"Checking file: {file_name}")
        if re.match(pattern, file_name) and not file_name.startswith('._'):
            logging.debug(f"Matched file in Downloads: {file_name}")
            file_path = os.path.join(downloads_dir, file_name)
            target_path = os.path.join(bdc_subdir, file_name)
            if os.path.exists(target_path):
                if os.path.getsize(file_path) == os.path.getsize(target_path):
                    logging.debug(f"File already exists with same name and size: {file_name}")
                    os.remove(file_path)
                    continue
                else:
                    logging.debug(f"Removing older file: {target_path}")
                    os.remove(target_path)
            logging.debug(f"Moving file: {file_path} to {target_path}")
            shutil.move(file_path, target_path)
            files_moved = True

    if not files_moved:
        logging.debug(f"No FCC bdc files found for state {fips_code} in Downloads directory.")
        print(f"No FCC bdc files found for state {fips_code} in Downloads directory.")

def get_latest_bdc_files(state_dir, fips_code):
    pattern = re.compile(BDC_SRC_FILE_PATTERN.replace(r'\d{2}', fips_code, 1))
    latest_files = {}

    for file_name in os.listdir(state_dir):
        match = pattern.match(file_name)
        if match:
            base_name = match.group(1)
            date_str = match.group(2)
            try:
                date_obj = datetime.strptime(date_str, '%d%b%Y')
                if base_name not in latest_files or date_obj > latest_files[base_name][1]:
                    latest_files[base_name] = (file_name, date_obj)
            except ValueError as e:
                logging.error(f"Error parsing date: {e} from file: {file_name} in path: {state_dir}")

    return [file_name for file_name, _ in latest_files.values()]

def create_symbolic_links(state_dir, bdc_subdir, bdc_file_list):
    version_pattern = r"_[A-Z]\d{2}_\d{2}[a-z]{3}\d{4}"
    for file_name in bdc_file_list:
        alias_name = re.sub(version_pattern, '', file_name)
        symlink_path = os.path.join(state_dir, alias_name)
        target_path = os.path.join(bdc_subdir, file_name)
        if os.path.exists(symlink_path):
            logging.debug(f"Removing existing symlink: {symlink_path}")
            os.remove(symlink_path)
        logging.debug(f"Creating symlink: {symlink_path} -> {target_path}")
        os.symlink(target_path, symlink_path)

def create_state_directory_and_move_files():
    states_to_process = STATES_AND_TERRITORIES
    if args.state:
        states_to_process = [state for state in STATES_AND_TERRITORIES if state[1] in args.state]

    for fips_code, abbr, name in states_to_process:
        print(f"Processing state: {abbr} ({name})")
        state_dir = os.path.join(bdc_dir, f"{fips_code}_{abbr}_{name.replace(' ', '_')}")
        bdc_subdir = os.path.join(state_dir, 'bdc')
        
        # Create state directory if it does not exist
        if not os.path.exists(state_dir):
            logging.debug(f"Creating directory: {state_dir}")
            os.makedirs(state_dir)
        
        # Remove existing symbolic links
        remove_existing_symlinks(state_dir)
        
        # Move files from Downloads to the state directory
        move_files_from_downloads(state_dir, fips_code)
        
        bdc_file_list = get_latest_bdc_files(bdc_subdir, fips_code)
        if bdc_file_list:
            create_symbolic_links(state_dir, bdc_subdir, bdc_file_list)
        else:
            logging.debug(f"No BDC files found for state {abbr} ({name})")

if __name__ == "__main__":
    create_state_directory_and_move_files()