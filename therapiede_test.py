import sys
import os

currentScriptDirectoryPath = os.path.dirname(os.path.abspath(__file__))
currentScriptDirectoryPathFiles = os.listdir(currentScriptDirectoryPath)

sys.path.append(currentScriptDirectoryPath)

from therapiede_list_lib import write_trans_db_files

no_trans_profil = {}
trans_profil = {}   
ret_write_trans_db_files = write_trans_db_files()
trans_profil = ret_write_trans_db_files["trans_profil"]
no_trans_profil = ret_write_trans_db_files["no_trans_profil"]