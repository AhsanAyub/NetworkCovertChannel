__author__ = "Md. Ahsan Ayub"
__license__ = "GPL"
__credits__ = ["Ayub, Md. Ahsan", "Smith, Steven", "Siraj, Ambareen",
                    "Hope, Shelby"]
__maintainer__ = "Md. Ahsan Ayub"
__email__ = "mayub42@students.tntech.edu"
__status__ = "Prototype"

# Importing the libraries
import pandas as pd

# Parsing data from the production JSON dataset
dataset = pd.read_csv('dns-traffic.20150626.txt', sep=' ', error_bad_lines=False, header=None)

# Generating the CSV file for further usuage.            
pd.DataFrame(dataset).to_csv("DNS_Reg_Traffic.csv")