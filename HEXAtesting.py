from urllib.request import urlopen

#Global Variables
myurl="http://hexa-a.com/offline/"
okStamp="Ok"

class ToolTesting:
  def __init__(self):
    pass

  def remove_endlines(self, orignal_data):
    new_data=[]
    for i in orignal_data:
        if not isinstance(i, str):
            i=i.decode("utf-8")
        temp_data=i.replace('\r','')
        temp_data=temp_data.replace('\n','')
        if temp_data!="":
            new_data.append(temp_data)
    return new_data

  def open_Offline_Cases(self, inFile):
    try:
        offline_File=open(inFile,'r')
        offline_File_Data=self.remove_endlines(offline_File.readlines())
        offline_File.close()
        if len(offline_File_Data)<2:
            raise IOError
        return offline_File_Data
    except IOError:
        return -1

  def split_Data(self, file_Name,data_In):
    data_Out_Input=[]
    data_Out_Answer=[]
    for l in range(len(data_In)):
        if l%2==0:
            data_Out_Input.append([])
            data_Out_Input[int(l/2)].append(file_Name)
            for x in range(len(data_In[l].split())):
                data_Out_Input[int(l/2)].append(data_In[l].split()[x])
        else:
            data_Out_Answer.append(data_In[l])
    return data_Out_Input,data_Out_Answer

  def download_Other_Files(self):
    try:
        #Get File names to download
        online_Files = urlopen(myurl+"Files.hexa")
        online_Files_Content = self.remove_endlines(online_Files.readlines())
        #Check that online data is been read successfully
        if(online_Files_Content[0]!=okStamp):
            raise ValueError
        del online_Files_Content[0]                         #Erase Ok stamp
        #Download each file
        for i in online_Files_Content:
            #Repeat what we done before with each file
            online_File_to_Download = urlopen(myurl+i)
            online_File_to_Download_Content = self.remove_endlines(online_File_to_Download.readlines())
            if(online_File_to_Download_Content[0]!=okStamp):
                raise ValueError
            del online_File_to_Download_Content[0]
            offline_File_to_Save=open(i,'w+')
            for j in online_File_to_Download_Content:
                offline_File_to_Save.write(j+"\n")
            offline_File_to_Save.close()
    except:
        return "Error while updating, Can\'t download all files!"
    else:
        return "Files Updated Successfully"

  def concat(self, inlist):
    outstring=""
    for i in inlist:
        outstring = outstring + " " + i
    return outstring