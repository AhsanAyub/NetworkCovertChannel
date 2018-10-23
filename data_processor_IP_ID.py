__author__ = "Md. Ahsan Ayub"
__license__ = "GPL"
__credits__ = ["Ayub, Md. Ahsan", "Smith, Steven", "Siraj, Ambareen",
                    "Hope, Shelby"]
__maintainer__ = "Md. Ahsan Ayub"
__email__ = "mayub42@students.tntech.edu"
__status__ = "Prototype"

# Importing the libraries
import numpy as np
import pandas as pd
import json

'''
Structure of the JSON dataset:
    1st Layer node = 4 
    - Key = _index, _score, _source and _type
    2nd Layer of interest is _source | node = 4
    - Key = _eth, frame, ip and tcp
    3rd Layer of interet is ip | key =
    - Key = ip.hdr_len, ip.len, ip.id, ip.flags, ip.checksum, ip.checksum.status, ip.flags.rb, ip.flags.df,
    ip.flags.mf, ip.frag_offset, ip.ttl, ip.proto
'''

# Initializing the globals
columnName = ['ip.hdr_len', 'ip.len', 'ip.id', 'ip.flags', 'ip.checksum', 'ip.checksum.status', 'ip.flags.rb', 'ip.flags.df', 'ip.flags.mf', 'ip.frag_offset', 'ip.ttl', 'ip.proto', 'class']
mainDataFrame = np.ndarray([100000,13])
mainDataFrame = mainDataFrame.astype(str)
temp = ['nan' for i in range(13)]
rowIndexToInsertNDArray = 0

# Index Checking of the existing column
def checkColumnName(key):
    for i in range(0, 13):
        if (key == columnName[i]):
            return i # returning the existing value index
    return -1 # if no item exists 

def loadToMainDataFrame():
    for i in range(13):
        if(temp[i] == 'nan'):
            mainDataFrame[rowIndexToInsertNDArray][i] = np.nan
        else:
            mainDataFrame[rowIndexToInsertNDArray][i] = temp[i]

# Parsing data from the production JSON dataset
data = json.load(open("./Production_Data_IP_ID_10_19_2018.json"))
for data_dic in data:
    for key in data_dic:
        if (key == '_source'):
            for key_2nd_Layer in data_dic[key]['layers']:
                if (key_2nd_Layer == 'ip'):
                    for final_key in data_dic[key]['layers'][key_2nd_Layer]:
                        if(final_key == 'ip.dsfield_tree'):
                            continue
                        elif(final_key == 'ip.flags_tree'):
                            for flags_tree in data_dic[key]['layers'][key_2nd_Layer][final_key]:
                                index = checkColumnName(flags_tree)
                                if (index == -1):
                                    continue
                                else:
                                    temp[index] = data_dic[key]['layers'][key_2nd_Layer][final_key][flags_tree]
                        else:
                            index = checkColumnName(final_key)
                            if (index == -1):
                                continue
                            else:
                                temp[index] = data_dic[key]['layers'][key_2nd_Layer][final_key]
                else:
                    continue
            
            # hard coded class defined
            if (temp[2] == '0x00002000'):
                temp[12] = 1 # No covert channel's presence
            else:
                temp[12] = 0 # Covert channel's presence
            loadToMainDataFrame()
            rowIndexToInsertNDArray = rowIndexToInsertNDArray + 1
            temp.clear()
            temp = ['nan' for i in range(13)]
        else:
            continue

# Generating the CSV file for further usuage.            
pd.DataFrame(mainDataFrame).to_csv("file_path.csv")
