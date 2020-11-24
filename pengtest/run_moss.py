from pengtest.moss import MossUtil
import os
from pengtest.moss_wrapper import MossEnvWrapper
import argparse
import sys
from dotenv import load_dotenv


# Version Number for Release
VERSION_NUM = '0.9.9.4'


def env_setup():
    m = MossEnvWrapper()
    print("-=- Welcome to the Moss Key setup tool, you will be prompted to enter your Moss key -=-")
    m.populate_env()


# handle command line args
def parse_arguments():
    parser = argparse.ArgumentParser(description='A program to run Stanford moss on student submitted projects. Operates by taking in folder of base files and folders of submissions, positional arguemnts: language, basefiles, submissions')
    parser.add_help = True
    parser.add_argument('language', nargs='?', help='language to test with')
    parser.add_argument('basefiles', nargs='?', default="./basefiles", help='path of folder containing base files that you provided to students (default ./basefiles)')
    parser.add_argument('submissions', nargs='?', default="./submissions", help='path of folder containing student submissions (default ./submissions)')
    parser.add_argument('-V', '-v', '--version', action='version', version='%(prog)s ' + str(VERSION_NUM))
    parser.add_argument('-S', '-s', '--setupenv', action='store_true', help='Run the setup wizard for MOSS API Key Environment Variables')
    config = parser.parse_args(sys.argv[1:])
    config.logformat = "%(message)s"
    return config


def main():
    print("-=- Running Stanford Moss CLI tool -=-")

    arg_config = parse_arguments()
    if arg_config.setupenv == True:
        env_setup()
    
    moss_obj = MossUtil("moss.env")

    if arg_config.language != None:
        moss_obj.init_moss("python")
    else:
        raise ValueError("No Language Provided")

    if arg_config.basefiles != None and arg_config.submissions != None:
        moss_obj.add_files("basefiles","submissions")
    
    moss_obj.send_files()
    moss_obj.save_files()


if __name__ == "__main__":
    main()