import argparse
from os.path import join, abspath, relpath, commonprefix, isdir, exists, dirname
import os
from shutil import rmtree, copytree, ignore_patterns
import re
import configparser

paths = set()

#A dir that contains the dir that contains this script - so that sc-machine/scripts/build_kb.py would become sc-machine
ostis_path = abspath(join(os.path.dirname(os.path.realpath(__file__)), "../"))

kb_scripts_path = join(ostis_path, "scripts/kb_scripts")

prepare_scripts = [
    join(kb_scripts_path, 'remove_scsi.py'),
    join(kb_scripts_path, 'gwf_to_scs.py')
]


REPO_FOLDER = "repo_folder"
OUTPUT_PATH = "output_path"
LOGFILE_PATH = "errors_file_path"
REPO_FILENAME = "repo_file_name"
CONFIG_PATH = "config_file_path"


def search_knowledge_bases(root_path: str, output_path: str, filename: str):
    if isdir(root_path):
        try:
            with open(join(root_path, filename), 'r') as root_file:
                for line in root_file.readlines():
                    line = line.replace('\n', '')
                    absolute_path = abspath(join(root_path, line))
                    # note: with current implementation, line is considered a comment if it's the first character in the line
                    #ignore paths we've already checked, comments and empty lines
                    if absolute_path in paths or line.startswith('#') or re.match(r"^\s*$", line):
                       continue
                    else:
                        paths.add(absolute_path)
                        search_knowledge_bases(
                        absolute_path, output_path, filename)
        except FileNotFoundError:
            #this branch will be used when a subsequent KB doesn't have any dependencies
            pass
    else:
        print("Folder", root_path, "is not found.")
        exit(1)


def copy_kb(output_path: str):
    prepared_kb = join(output_path, "prepared_kb")
    try:
        common_prefix = commonprefix(list(paths))
        for path in paths:
            # removes the common part from paths and copies what's left to prepared_kb
            copytree(path, join(prepared_kb, relpath(
                path, common_prefix)), ignore=ignore_patterns(".git"), dirs_exist_ok=True)
    except Exception as e:
        print(e)


def parse_config(path: str) -> dict:
    config_dict = {REPO_FOLDER: '', OUTPUT_PATH: '', LOGFILE_PATH: ''}
    config = configparser.ConfigParser()
    config.read(path)
    config_dict.update({OUTPUT_PATH: abspath(join(dirname(path), config['Repo']['Path']))})
    config_dict.update({LOGFILE_PATH: abspath(join(dirname(path), config['Repo']['Logfile'], "prepare.log"))})

    return config_dict


def prepare_kb(kb_to_prepare: str, logfile: str):
    for script in prepare_scripts:
        os.system('python3 ' + script + ' ' + kb_to_prepare + ' ' + logfile)
    if exists(logfile):
        print("Error while executing prepare_kb scripts. Check " + logfile + " for logs")
        exit(1)


def build_kb(bin_folder: str, kb_to_build: str):
    bin_folder = join(bin_folder, "kb.bin")
    os.makedirs(bin_folder, exist_ok=True)
    # call sc-builder with required parameters
    os.system(" ".join([join(ostis_path, "bin/sc-builder"), "-f", "-c", "-i", kb_to_build, "-o", bin_folder, "-e", join(ostis_path, "bin/extensions")]))



def main(args: dict):
    conf = parse_config(args[CONFIG_PATH])

    #absolutize paths passed as flags

    #rewrite options which were given by flags
     
    for key in args.keys():
        if args[key] is not None:
            if key in [REPO_FOLDER, OUTPUT_PATH, LOGFILE_PATH]: 
                flag = abspath(join(os.getcwd(), args[key]))
            else: flag = args[key] 
            conf[key] = flag
    # output the final configuration for the script, just to be sure about what's going on.
    print("args:", conf)

    # prepared_kb will appear in the same folder as kb.bin
    kb_to_prepare = join(conf[OUTPUT_PATH], "prepared_kb")
    if isdir(kb_to_prepare):
        rmtree(kb_to_prepare)

    search_knowledge_bases(conf[REPO_FOLDER], conf[OUTPUT_PATH], conf[REPO_FILENAME])

    if not paths:
        print("No KBs were found")
        exit(1)

    copy_kb(conf[OUTPUT_PATH])
    prepare_kb(kb_to_prepare, conf[LOGFILE_PATH])
    build_kb(conf[OUTPUT_PATH], kb_to_prepare)
    # rmtree(kb_to_prepare)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(dest=REPO_FOLDER, type=str,
                        help="The entrypoint folder, should contain a repo file, see -f option to change the name")

    parser.add_argument('-o', '--output', dest=OUTPUT_PATH,
                        help="Destination path - path where KB binaries will be stored. Taken from the config file unless overwritten by this flag.")

    parser.add_argument('-l', '--logfile', dest=LOGFILE_PATH,
                        help="Errors file path - in case of unsuccessful preparation, log will appear at this location. Taken from the config file unless overwritten by this flag.")

    parser.add_argument('-f', '--filename', dest=REPO_FILENAME,
                        help="Repo file name - a filename for repo file that will be used in all subsequent KBs. Default: repo.path", default="repo.path")

    parser.add_argument('-c', '--config', dest=CONFIG_PATH,
                        help="Config file path - path to the sc-machine config file (Note: config file has lower priority than flags!)")

    args = parser.parse_args()

    #convert args from namespace to a dict
    main(vars(args))
