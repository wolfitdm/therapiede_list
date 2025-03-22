import re


def get_valid_filename(name):
    s = str(name).strip().replace(" ", "_")
    s = re.sub(r"(?u)[^-\w.]", "_", s)
    return s


print(get_valid_filename('Sulzbach/ Saar_theras_online.txt'))