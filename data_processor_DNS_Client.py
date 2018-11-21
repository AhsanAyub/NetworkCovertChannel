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

# Initializing the globals
columnName = ['dns.id', 'dns.flags', 'dns.count.queries', 'dns.count.answers', 'dns.count.auth_rr', 'dns.count.add_rr', 'dns.qry.name', 'dns.qry.name.len', 'dns.count.labels', 'dns.qry.type', 'dns.qry.class', 'dns.resp.name', 'dns.resp.type', 'dns.resp.class', 'dns.resp.ttl', 'class']
mainDataFrame = np.ndarray([60500,16])
mainDataFrame = mainDataFrame.astype(str)
temp = ['nan' for i in range(16)]
rowIndexToInsertNDArray = 0

# Index Checking of the existing column
def checkColumnName(key):
    for i in range(0, 15):
        if (key == columnName[i]):
            return i # returning the existing value index
    return -1 # if no item exists 

def loadToMainDataFrame():
    for i in range(15):
        if(temp[i] == 'nan'):
            mainDataFrame[rowIndexToInsertNDArray][i] = np.nan
        else:
            mainDataFrame[rowIndexToInsertNDArray][i] = temp[i]

# Parsing data from the production JSON dataset
data = json.load(open("Filter_View_DNS_Packet_Client.json"))
for data_dic in data:
    for key in data_dic:
        if (key == '_source'):
            for key_2nd_Layer in data_dic[key]['layers']:
                if (key_2nd_Layer == 'dns'):
                    for final_key in data_dic[key]['layers'][key_2nd_Layer]:
                        if(final_key == 'Queries' or final_key == 'Answers'):
                            for dns_response in data_dic[key]['layers'][key_2nd_Layer][final_key]:
                                for dns_resonse_feature in data_dic[key]['layers'][key_2nd_Layer][final_key][dns_response]:
                                    index = checkColumnName(dns_resonse_feature)
                                    if (index == -1):
                                        continue
                                    else:
                                        temp[index] = data_dic[key]['layers'][key_2nd_Layer][final_key][dns_response][dns_resonse_feature]
                        else:
                            index = checkColumnName(final_key)
                            if (index == -1):
                                continue
                            else:
                                temp[index] = data_dic[key]['layers'][key_2nd_Layer][final_key]
                else:
                    continue
            
            # hard coded class defined
            temp[15] = 1 # Covert channel's presence
            loadToMainDataFrame()
            rowIndexToInsertNDArray = rowIndexToInsertNDArray + 1
            temp.clear()
            temp = ['nan' for i in range(18)]
        else:
            continue

# Generating the CSV file for further usuage.            
pd.DataFrame(mainDataFrame).to_csv("Processed_Data_Set_DNS_Client_20_11_2018.csv")