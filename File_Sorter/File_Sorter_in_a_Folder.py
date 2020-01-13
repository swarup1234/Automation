#!/usr/bin/env python
# coding: utf-8

# In[59]:


# Importing libraries
import os


# In[60]:


# Getting the working directory and moving to the wd
os.chdir("C:\\Users\\91990\\Downloads")


# In[68]:


# Getting a file list and folder names from the files
def get_filelist(path_val =os.getcwd()):
    val = []
    # Getting a list of files in the folder that are not temporary
    file_list = [x for x,y in map(lambda x: (x,"~$" in x), os.listdir()) if y==False]

    # Getting the list of file extensitons 
    for file_name in file_list:
        val.append(file_name.split(".")[-1])

    # Getting a list of values that have less than 4 values in its extension
    folder_list = [x.upper() for x,y in map(lambda x: (x,len(x)),set(val)) if y<=4]
    
    # Returing the output
    return({"folder_list":folder_list,"file_list":file_list})


# In[70]:


# Getting the list of files 
tempobj = get_filelist()
folder_list = tempobj["folder_list"]
file_list = tempobj["file_list"]


# In[71]:


# Moving the Files to the relevant folders
for folder_name in folder_list:
    file_path = os.getcwd()+"\\"+str(folder_name)
    
    # Creating the folders if they don't exist
    if(not os.path.exists(file_path)):
        print("Path doesn't exist for ",file_path)
        os.mkdir(file_path)
    
    # Getting the list of all the files with the similar names 
    file_list_to_move =[x for x,y in map(lambda x: (x,folder_name==x.upper().split(".")[-1] and not os.path.isdir(x)),file_list) if y==True]
    
    # Moving the files
    if len(file_list_to_move)>0:
        for file_to_move in file_list_to_move:
            os.rename(os.getcwd()+"\\"+str(file_to_move),os.getcwd()+'\\'+folder_name+"\\"+str(file_to_move))
    
    # Printing the output
    print({folder_name:file_list_to_move})
        

