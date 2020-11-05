import mosspy
import os
from dotenv import load_dotenv

class MossUtil:
    def __init__(self, dotenv_path, language):
        load_dotenv(dotenv_path)  # load token from .env file
        self.userid = os.getenv("USERID")

    # Returns mosspy object bound to userid and language
    # Language choices:
    # language_list = ["c", "cc", "java", "ml", "pascal", "ada",
    # "lisp", "scheme", "haskell", "fortran",
    # "ascii", "vhdl", "perl", "matlab", "python",
    # "mips", "prolog", "spice", "vb", "csharp",
    # "modula2", "a8086", "javascript", "plsql", "verilog"]
    def init_moss(self, language):
        self.moss_obj = mosspy.Moss(self.userid, language)

    # Adds files to be sent with submission
    def add_files(self):
        self.moss_obj.addBaseFile("submission/a01.py")
        self.moss_obj.addBaseFile("submission/test_student.py")

        # Submission Files
        self.moss_obj.addFile("submission/a01-sample.py")
        self.moss_obj.addFilesByWildcard("submission/a01-*.py")

    # Sends files via url created with moss_obj
    def send_files(self):
        self.url = self.moss_obj.send() # Submission Report URL

        print ("Report Url: " + self.url)

    def save_files(self):
        # Save report file
        self.moss_obj.saveWebPage(self.url, "submission/report.html")

        # Download whole report locally including code diff links
        mosspy.download_report(self.url, "submission/report/", connections=8)