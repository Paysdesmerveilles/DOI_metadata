#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 09:15:57 2016

@author: Alice FREMAND
"""

def xml(data):
    from lxml import etree
    from copy import deepcopy    
    # The variables are uploadede via the online form DOI_index03.html
    #############################################################
    ###############PROCESSING OF THE XML#########################
    ############################################################# 
    # the first step is to 
    doc = etree.parse('Template_DOI.xml')
    #doc = etree.parse('Metadata_template3.xml')
    root = doc.getroot()
    tree = etree.ElementTree(root)
    
    DOI_xml = root.find('{http://datacite.org/schema/kernel-3}identifier')
    #author_xml= root.find('{http://datacite.org/schema/kernel-3}creatorName')
    creators_xml = root.find('{http://datacite.org/schema/kernel-3}creators')
    for creators in creators_xml:
         author_xml= creators.find('{http://datacite.org/schema/kernel-3}creatorName')
         orcid_xml = creators.find('{http://datacite.org/schema/kernel-3}nameIdentifier')
         affiliation_xml = creators.find('{http://datacite.org/schema/kernel-3}affiliation')
    title_xml = root.find('{http://datacite.org/schema/kernel-3}titles')[0]
    subtitle_xml = root.find('{http://datacite.org/schema/kernel-3}titles')[1]
    publisher_xml = root.find('{http://datacite.org/schema/kernel-3}publisher')
    year_xml = root.find('{http://datacite.org/schema/kernel-3}publicationYear')
    subject_xml = root.find('{http://datacite.org/schema/kernel-3}subjects')
    contributors_xml = root.find('{http://datacite.org/schema/kernel-3}contributors')
    for contributors in contributors_xml:
         contributor_xml= contributors.find('{http://datacite.org/schema/kernel-3}contributorName')
         contributor_orcid_xml = contributors.find('{http://datacite.org/schema/kernel-3}nameIdentifier')
         contributor_affiliation_xml = contributors.find('{http://datacite.org/schema/kernel-3}affiliation')
    date_xml = root.find('{http://datacite.org/schema/kernel-3}dates')[0]
    language_xml = root.find('{http://datacite.org/schema/kernel-3}language')
    datatype_xml = root.find('{http://datacite.org/schema/kernel-3}resourceType')
    datatypeText_xml = root.find('{http://datacite.org/schema/kernel-3}resourceType')
    url_xml = root.find('{http://datacite.org/schema/kernel-3}alternateIdentifiers')[0]
    
    size_xml = root.find('{http://datacite.org/schema/kernel-3}sizes')
    format1_xml = root.find('{http://datacite.org/schema/kernel-3}formats')
    version_xml = root.find('{http://datacite.org/schema/kernel-3}version')
    
    license_xml = root.find('{http://datacite.org/schema/kernel-3}rightsList')
    licenseText_xml = root.find('{http://datacite.org/schema/kernel-3}rightsList')[0]
    abstract_xml = root.find('{http://datacite.org/schema/kernel-3}descriptions')
    loc_xml = root.find('{http://datacite.org/schema/kernel-3}geoLocations')
    for loc in loc_xml:
         geoPoint_xml= loc.find('{http://datacite.org/schema/kernel-3}geoLocationPoint')
         geoBox_xml = loc.find('{http://datacite.org/schema/kernel-3}geoLocationBox')
         geoPlace_xml = loc.find('{http://datacite.org/schema/kernel-3}geoLocationPlace')
    relations_xml = root.find('{http://datacite.org/schema/kernel-3}relatedIdentifiers')


    #############################################################
    ###############  ASSOCIATE VALUE FROM FORM ##################
    #############################################################  

    #Required data

    DOI_xml.text = data['doi']
    url_xml.text = data['url']
    authorCounter = len([a for a in data.keys() if a.startswith('authorName')])
    contributorCounter = len([a for a in data.keys() if a.startswith('contributorName')])
    subjectCounter = len([a for a in data.keys() if a.startswith('subject')])
    relationCounter = len([a for a in data.keys() if a.startswith('relatedID')])
    for i in range(0, authorCounter - 1):
        author_xml.getparent().addnext(deepcopy(author_xml.getparent()))
    for i in range(0, authorCounter ):
#        if 'authorFirstname%d' %i in data.keys():       
#            creators_xml[i][0].text = data['authorName%d' %i] +', ' + data['authorFirstname%d' %i]
#        else:
        creators_xml[i][0].text = data['authorName%d' %i]
        if 'authorOrcid%d' %i in data.keys():
            creators_xml[i][1].text = data['authorOrcid%d' %i]
            if 'authorAffiliation%d' %i in data.keys():
                creators_xml[i][2].text = data['authorAffiliation%d' %i]
            else:
                creators_xml[i][2].getparent().remove(creators_xml[i][2])
        else:
            creators_xml[i][1].getparent().remove(creators_xml[i][1])
            if 'authorAffiliation%d' %i in data.keys():
                creators_xml[i][1].text = data['authorAffiliation%d' %i]
            else:
                creators_xml[i][1].getparent().remove(creators_xml[i][1])
            
#    publisher_xml.text = publisher.decode('utf-8')

    publisher_xml.text = data['publisher0']
#    for i in range(1, publisherCounter):
#        publisher_xml.getparent().addnext(deepcopy(publisher_xml.getparent()))          
#        publisher_xml.getparent()[i].text = data['publisher%d' %i]
    year_xml.text= str(data['year'])
    title_xml.text = data['title']
    #end required data
    removeXML_from_dict('subtitle', data, subtitle_xml)

    if contributorCounter == 0:
        contributors_xml.getparent().remove(contributors_xml)
    else:
        for i in range(0, contributorCounter - 1):
            contributors_xml[0].addnext(deepcopy(contributors_xml[0]))
        for i in range(0, contributorCounter ):
            contributors_xml[i][0].text = data['contributorName%d' %(i+1)]
            if 'contributorType%d' %(i+1) in data.keys():       
                contributors_xml[i].attrib['contributorType'] = data['contributorType%d' %(i+1)]
#            if 'contributorFirstname%d' %(i+1) in data.keys():       
#                contributors_xml[i][0].text = data['contributorName%d' %(i+1)] +', ' + data['contributorFirstname%d' %(i+1)]
#            else:
#                 contributors_xml[i][0].text = data['contributorName%d' %(i+1)]
            if 'contributorOrcid%d' %(i+1) in data.keys():
                contributors_xml[i][1].text = data['contributorOrcid%d' %(i+1)]
                if 'contributorAffiliation%d' %(i+1) in data.keys():
                    contributors_xml[i][2].text = data['contributorAffiliation%d' %(i+1)]
                else:
                    contributors_xml[i][2].getparent().remove(contributors_xml[i][2])
            else:
                contributors_xml[i][1].getparent().remove(contributors_xml[i][1])
                if 'contributorAffiliation%d' %(i+1) in data.keys():
                    contributors_xml[i][1].text = data['contributorAffiliation%d' %(i+1)]
                else:
                    contributors_xml[i][1].getparent().remove(contributors_xml[i][1])
    if subjectCounter == 0:
        subject_xml.getparent().remove(subject_xml)
    else:
        subject_xml[0].text = data['subject0']
        for i in range(1, subjectCounter):
            subject_xml[0].addnext(deepcopy(subject_xml[0]))          
            subject_xml[i].text = data['subject%d' %i]                        

#    date_xml.text = str(datetime.now().strftime('%Y-%m-%d'))
    if 'language' in data.keys():
        language_xml.text = data['language'] 
    datatype_xml.attrib['resourceTypeGeneral'] =  data['datatype']
    if 'datatypeText' in data.keys():
        datatypeText_xml.text = data['datatypeText']
    removeXML_fields('size', data, size_xml)
    removeXML_fields('format1', data, format1_xml)
    removeXML_from_dict('version', data, version_xml)    
    if data['license'] == 'None':
        license_xml.getparent().remove(license_xml)
    else:
        licenseText_xml.text = data['license']
        if data['license'].endswith('(CC-BY 4.0)'):
            license_xml[0].attrib['rightsURI'] = 'http://creativecommons.org/licenses/by/4.0/'
        elif data['license'].endswith('(CC BY-SA 4.0)'):
            license_xml[0].attrib['rightsURI'] = 'https://creativecommons.org/licenses/by-sa/4.0/'
        elif data['license'].endswith('(CC BY-ND 4.0)'):
            license_xml[0].attrib['rightsURI'] = 'https://creativecommons.org/licenses/by-nd/4.0/'
        elif data['license'].endswith('(CC BY-NC 4.0)'):
            license_xml[0].attrib['rightsURI'] = 'https://creativecommons.org/licenses/by-nc/4.0//'
        elif data['license'].endswith('(CC BY-NC-SA 4.0)'):
            license_xml[0].attrib['rightsURI'] = 'https://creativecommons.org/licenses/by-nc-sa/4.0/'
        elif data['license'].endswith('(CC BY-NC-ND 4.0)'):
            license_xml[0].attrib['rightsURI'] = 'https://creativecommons.org/licenses/by-nc-nd/4.0/'

    removeXML_fields('abstract',data, abstract_xml)
    
    if relationCounter == 0:
        relations_xml.getparent().remove(relations_xml)
    else:
        for i in range(0, relationCounter - 1):
            relations_xml[0].addnext(deepcopy(relations_xml[0]))
        for i in range(0, relationCounter):
            relations_xml[i].text = data['relatedID%d' %(i+1)]
            if 'relationType%d' %(i+1) in data.keys():       
                relations_xml[i].attrib['relationType'] = data['relationType%d' %(i+1)]
            if 'relationIDtype%d' %(i+1) in data.keys():       
                relations_xml[i].attrib['relatedIdentifierType'] = data['relationIDtype%d' %(i+1)]      
               
    if ['longitude' in data.keys() and 'latitude' in data.keys()] or ['north' in data.keys() and 'south' in data.keys() and 'east' in data.keys() and 'west' in data.keys()] or 'location' in data.keys():
        if 'longitude' in data.keys() and 'latitude' in data.keys():
            geoPoint_xml.text = str(data['longitude']) + ' '+ str(data['latitude'])            
        else:
            geoPoint_xml.getparent().remove(geoPoint_xml)
        if 'north' in data.keys() and 'south' in data.keys() and 'east' in data.keys() and 'west' in data.keys():
            geoBox_xml.text= str(data['east']) + ' '+ str(data['north']) + ' '+str(date['west']) + ' ' + str(data['south'])
        else:
            geoBox_xml.getparent().remove(geoBox_xml)
    else:
        loc_xml.getparent().remove(loc_xml)    
    removeXML_from_dict('location', data, geoPlace_xml)
    doc.write('File/XML_temp.xml', xml_declaration=True, encoding = 'utf-8')
    
    
def removeXML_field(formvalue, field_xml):
    if formvalue is None:
        field_xml.getparent().remove(field_xml)
    else:
        field_xml.text = formvalue
        
def removeXML_from_dict(formvalue, dict1, field_xml):
    if formvalue in dict1.keys():
        field_xml.text = dict1[formvalue]
    else:
        field_xml.getparent().remove(field_xml)
        
def removeXML_fields(formvalue, dict1, field_xml):
    if formvalue in dict1.keys():
        field_xml[0].text =  dict1[formvalue]
    else:
        field_xml.getparent().remove(field_xml)