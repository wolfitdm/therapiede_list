import sys
import os

currentScriptDirectoryPath = os.path.dirname(os.path.abspath(__file__))
currentScriptDirectoryPathFiles = os.listdir(currentScriptDirectoryPath)

sys.path.append(currentScriptDirectoryPath)

from therapiede_list_lib import write_trans_db_files
from therapiede_list_lib import write_all_trans_online_theras
#write_all_trans_online_theras(True)
write_trans_db_files(False)