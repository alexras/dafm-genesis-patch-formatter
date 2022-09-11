#!/usr/bin/env python3

import argparse
import os
import pprint
import shutil

DMP_PATCH_SIZE_BYTES = 51
MAX_BANK_SIZE = 128

def format_patches(input_dir, output_dir):
    banks = []
    current_bank = []

    for dir_path, child_dirs, filenames in os.walk(input_dir):
        for filename in filenames:
            if os.path.splitext(filename)[1].lower() == '.dmp':
                file_abspath = os.path.join(dir_path, filename)
                if os.path.getsize(file_abspath) == DMP_PATCH_SIZE_BYTES:
                    current_bank.append(file_abspath)

                if len(current_bank) == MAX_BANK_SIZE:
                    banks.append(current_bank)
                    current_bank = []

    if len(current_bank) > 0:
        banks.append(current_bank)

    for bank_number, bank in enumerate(banks):
        bank_dir = os.path.join(output_dir, f'bank{bank_number:03d}')
        os.makedirs(bank_dir, exist_ok=True)

        with open(os.path.join(bank_dir, 'bank-manifest.txt'), 'w+') as fp:
            for patch_number, patch_file in enumerate(bank):
                shutil.copyfile(patch_file, os.path.join(bank_dir, f'instr{patch_number:03d}.dmp'))
                fp.write(f'{patch_number:03d} - {patch_file}\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir', help='directory containing patches to format')
    parser.add_argument('output_dir', help='directory to which to output formatted patches')

    args = parser.parse_args()

    format_patches(**vars(args))
