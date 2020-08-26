# fetch roles and members through jazn-data.xml

import xml.etree.ElementTree as ET
import pandas as pd

tree = ET.parse('D:\data.xml') # re-point to jazn file (11g fmwconfig, 12c bar file) 
root = tree.getroot()
   
def get_type(text):
    if text == 'weblogic.security.principal.WLSGroupImpl':
        return 'Group'
    elif text == 'oracle.security.jps.service.policystore.ApplicationRole':
        return 'Role'
    else:
        return 'User'

# find method does not work well; nested loop creates hierarchical data-structure
# findall method to traverse root has difficulties as name tag is repeated multiple times
# create multiple lists and append searched attributes

rolename,displayname,description,memname,memtype=[],[],[],[],[]
for item in root.getchildren()[1].getchildren()[0].getchildren()[0].getchildren()[1].getchildren():
    rname=item.findtext('name')
    dname=item.findtext('display-name')
    desc=item.findtext('description')
    #print ('\n')
    #print(rname, ',', dname, ',', desc, ',', end= ' ')
    for things in item.findall('members/member'):
        mname = things.findtext('name')
        m_type = things.findtext('class')
        mtype = get_type(m_type) # call get_type to fetch correct member type
        #print('\n')
        #print (rname, ',', dname, ',', desc, ',', mname, ',',mtype, ';', end= ' ')
        rolename.append(rname)
        displayname.append(dname)
        description.append(desc)
        memname.append(mname)
        memtype.append(mtype)
		
#construct dataframe from lists
df = pd.DataFrame(data={"Role-Name": rolename, "Display-Name": displayname,
                        "Description": description, "Member-Name": memname, "Member-Type": memtype })
#print(list(df.columns.values))
frame = df[['Role-Name', 'Display-Name', 'Description', 'Member-Name', 'Member-Type' ]] # reordering dataframe columns
frame.to_csv("fileop.csv", sep=',',index=False) # re-point to export file/location