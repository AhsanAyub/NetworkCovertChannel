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
    3rd Layer of interet is tcp
    - Key == 'tcp.seq', 'tcp.nxtseq', 'tcp.ack', 'tcp.hdr_len', 'tcp.flags', 'tcp.flags.res', 'tcp.flags.ns',
             'tcp.flags.cwr', 'tcp.flags.ecn', 'tcp.flags.urg', 'tcp.flags.ack', 'tcp.flags.push', 'tcp.flags.reset',
             'tcp.flags.syn', 'tcp.flags.fin', 'tcp.checksum', 'tcp.checksum.status', 'tcp.urgent_pointer', 'class'
'''

# Initializing the globals
columnName = ['tcp.seq', 'tcp.nxtseq', 'tcp.ack', 'tcp.hdr_len', 'tcp.flags', 'tcp.flags.res', 'tcp.flags.ns', 'tcp.flags.cwr', 'tcp.flags.ecn', 'tcp.flags.urg', 'tcp.flags.ack', 'tcp.flags.push', 'tcp.flags.reset', 'tcp.flags.syn', 'tcp.flags.fin', 'tcp.checksum', 'tcp.checksum.status', 'tcp.urgent_pointer', 'class']
mainDataFrame = np.ndarray([100000,19])
mainDataFrame = mainDataFrame.astype(str)
temp = ['nan' for i in range(19)]
rowIndexToInsertNDArray = 0

# Index Checking of the existing column
def checkColumnName(key):
    for i in range(0, 19):
        if (key == columnName[i]):
            return i # returning the existing value index
    return -1 # if no item exists 

def loadToMainDataFrame():
    for i in range(19):
        if(temp[i] == 'nan'):
            mainDataFrame[rowIndexToInsertNDArray][i] = np.nan
        else:
            mainDataFrame[rowIndexToInsertNDArray][i] = temp[i]

# Parsing data from the production JSON dataset
data = json.load(open("Regular_Network_Traffic.json"))
for data_dic in data:
    for key in data_dic:
        if (key == '_source'):
            for key_2nd_Layer in data_dic[key]['layers']:
                '''print(key_2nd_Layer)'''
                if (key_2nd_Layer == 'tcp'):
                    for final_key in data_dic[key]['layers'][key_2nd_Layer]:
                        #print(final_key)
                        if(final_key == 'tcp.flags_tree'):
                            for flags_tree in data_dic[key]['lX ayers'][key_2nd_Layer][final_key]:
                                index = checkColumnName(flags_tree)
                                if (index == -1):
                                    continue
                                else:
                                    #print(temp[index])
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
            '''if (temp[0] == '536870912'):'''
            temp[18] = 1 # Covert channel's presence
            '''else:
                temp[18] = 0 # No Covert channel's presence'''
            loadToMainDataFrame()
            rowIndexToInsertNDArray = rowIndexToInsertNDArray + 1
            temp.clear()
            temp = ['nan' for i in range(19)]
        else:
            continue

# Generating the CSV file for further usuage.            
pd.DataFrame(mainDataFrame).to_csv("Processed_Data_Set_Regular_Traffic_TCP_Seq_30_11_2018.csv")