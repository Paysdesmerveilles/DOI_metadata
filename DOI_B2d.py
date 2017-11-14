#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 09:15:57 2016

@author: Alice FREMAND
"""

def xml2B2d(filePath):
    from lxml import etree
    import io
    
 ##############################################################
###################### XML PARSING  ##########################
############################################################# 
    doc = etree.parse(io.BytesIO(filePath))
    root = doc.getroot()
    tree = etree.ElementTree(root)
    data={}
    
    DOI_xml = root.find('{http://datacite.org/schema/kernel-3}identifier')
    data['doi'] = DOI_xml.text
    creators_xml = root.find('{http://datacite.org/schema/kernel-3}creators')
    #    for i in range(0, authorCounter - 1):
    #        author_xml.getparent().addnext(deepcopy(author_xml.getparent()))
    #    for i in range(0, authorCounter ):
    #        if 'authorFirstname%d' %i in data.keys():       
    #            creators_xml[i][0].text = data['authorName%d' %i] +', ' + data['authorFirstname%d' %i]
    creator_xml = []
    orcid_xml = []
    affiliation_xml = []
    data['authorCounter'] = len(creators_xml)
    for i in range(0, len(creators_xml)):
        for creators in creators_xml:
            creator_xml.append(creators.find('{http://datacite.org/schema/kernel-3}creatorName').text)
            orcid_xml.append(creators.find('{http://datacite.org/schema/kernel-3}nameIdentifier'))
            affiliation_xml.append(creators.find('{http://datacite.org/schema/kernel-3}affiliation'))
        data['authorName%d' %i] = creator_xml[i].encode('ascii', 'xmlcharrefreplace').decode('utf-8', 'ignore')
        if orcid_xml[i] != None:
            data['orcid%s' %i] = orcid_xml[i].text
        else:
            data['orcid%s' %i] = ''
        if affiliation_xml[i] != None:
            data['affiliation%s' %i] = affiliation_xml[i].text.encode('ascii', 'xmlcharrefreplace').decode('utf-8', 'ignore')
        else:
            data['affiliation%s' %i] = ''
            
    title_xml = root.find('{http://datacite.org/schema/kernel-3}titles')[0]
    data['title'] = title_xml.text.encode('ascii', 'xmlcharrefreplace').decode('utf-8', 'ignore')
    subtitle_xml = root.find('{http://datacite.org/schema/kernel-3}titles')[1]
    if subtitle_xml in locals():
        data['subtitle'] = subtitle_xml.text.encode('ascii', 'xmlcharrefreplace').decode('utf-8', 'ignore')
    else:
        data['subtitle'] = ''
    publisher_xml = root.find('{http://datacite.org/schema/kernel-3}publisher')
    data['publisher'] = publisher_xml.text.encode('ascii', 'xmlcharrefreplace').decode('utf-8', 'ignore')
    year_xml = root.find('{http://datacite.org/schema/kernel-3}publicationYear')
    data['year'] = year_xml.text
    subjects_xml = root.find('{http://datacite.org/schema/kernel-3}subjects')
    subject_xml = []
    
    if subjects_xml != None:
        data['subjectCounter'] = len(subjects_xml)
        for i in range(0, len(subjects_xml)):
            subject_xml.append(subjects_xml[i].text)
            data['subject%s' %i] = subject_xml[i].encode('ascii', 'xmlcharrefreplace').decode('utf-8', 'ignore')
        
    contributors_xml = root.find('{http://datacite.org/schema/kernel-3}contributors')
    contributor_xml = []
    contributor_orcid_xml = []
    contributor_affiliation_xml = []
    contributor_type_xml = []
    
    if contributors_xml != None:
        data['contributorCounter'] = len(contributors_xml)
        for i in range(0, len(contributors_xml)):
            for contributors in contributors_xml:
                 contributor_xml.append(contributors.find('{http://datacite.org/schema/kernel-3}contributorName'))
                 contributor_orcid_xml.append(contributors.find('{http://datacite.org/schema/kernel-3}nameIdentifier'))
                 contributor_affiliation_xml.append(contributors.find('{http://datacite.org/schema/kernel-3}affiliation'))
            data['contributorName%s' %i] = contributor_xml[i].text.encode('ascii', 'xmlcharrefreplace').decode('utf-8', 'ignore')
            if contributor_orcid_xml[i] !=  None:
                data['contributorOrcid%s' %i] = contributor_orcid_xml[i].text.encode('ascii', 'xmlcharrefreplace').decode('utf-8', 'ignore')
            if contributor_affiliation_xml[i] != None:
                data['contributorAffiliation%s' %i] = contributor_affiliation_xml[i].text.encode('ascii', 'xmlcharrefreplace').decode('utf-8', 'ignore')
            if contributors_xml[i].attrib['contributorType'] != None:
                data['contributorType%d' %i] = contributors_xml[i].attrib['contributorType']
    date_xml = root.find('{http://datacite.org/schema/kernel-3}dates')[0]
    language_xml = root.find('{http://datacite.org/schema/kernel-3}language')
    data['language'] = language_xml.text
    datatype_xml = root.find('{http://datacite.org/schema/kernel-3}resourceType')
    if datatype_xml != None:
        if datatype_xml.text != None:
            data['datatypeText'] = datatype_xml.text.encode('ascii', 'xmlcharrefreplace').decode('utf-8', 'ignore')
        else:
            data['datatypeText'] =''
        if datatype_xml.attrib['resourceTypeGeneral'] != None:
            data['datatype'] = datatype_xml.attrib['resourceTypeGeneral']
        else:
            data['datatype'] = ''
        
    url_xml = root.find('{http://datacite.org/schema/kernel-3}alternateIdentifiers')[0]
    data['url'] = url_xml.text
    size_xml = root.find('{http://datacite.org/schema/kernel-3}sizes')
    if size_xml != None:
        data['size'] = size_xml[0].text.encode('ascii', 'xmlcharrefreplace').decode('utf-8', 'ignore')
    else:
        data['size'] = ''
    format1_xml = root.find('{http://datacite.org/schema/kernel-3}formats')
    if format1_xml != None:
        data['format1'] = format1_xml[0].text.encode('ascii', 'xmlcharrefreplace').decode('utf-8', 'ignore')
    else:
        data['format1'] = ''
    version_xml = root.find('{http://datacite.org/schema/kernel-3}version')
    if version_xml != None:
        data['version'] = version_xml.text.encode('ascii', 'xmlcharrefreplace').decode('utf-8', 'ignore')
    else:
        data['version'] = ''
    license_xml = root.find('{http://datacite.org/schema/kernel-3}rightsList')
    if license_xml != None:
        data['license'] = license_xml[0].text
    else:
        data['license'] = 'None'
    abstract_xml = root.find('{http://datacite.org/schema/kernel-3}descriptions')
    if abstract_xml != None:
        data['abstract'] = abstract_xml[0].text.encode('ascii', 'xmlcharrefreplace').decode('utf-8', 'ignore')
    else:
        data['abstract'] =''
    loc_xml = root.find('{http://datacite.org/schema/kernel-3}geoLocations')
    if loc_xml != None:
        for loc in loc_xml:
             geoPoint_xml= loc.find('{http://datacite.org/schema/kernel-3}geoLocationPoint')
             geoBox_xml = loc.find('{http://datacite.org/schema/kernel-3}geoLocationBox')
             geoPlace_xml = loc.find('{http://datacite.org/schema/kernel-3}geoLocationPlace')
        if geoPoint_xml != None:
            data['longitude'], data['latitude'] = geoPoint_xml.text.split(' ')
        else:
            data['longitude']= ''
            data['latitude'] = ''
        if geoBox_xml != None:
            data['east'], data['north'], data['west'], data['south'] = geoBox_xml.text.split(' ')
        else:
            data['east'] = ''
            data['north'] = ''
            data['west'] = ''
            data['south'] = ''
        if geoPlace_xml != None:
            data['geoPlace'] = geoPlace_xml.text.encode('ascii', 'xmlcharrefreplace').decode('utf-8', 'ignore')
        else:
            data['geoPlace'] = 0
    relationType = []
    relatedID = []
    relationID = []
    relations_xml = root.find('{http://datacite.org/schema/kernel-3}relatedIdentifiers')
    if relations_xml != None:
        data['relationCounter'] = len(relations_xml)
        for i in range(0, len(relations_xml)):
            relationType.append(relations_xml[i].attrib['relationType'])
            relationID.append(relations_xml[i].text)
            relatedID.append(relations_xml[i].attrib['relatedIdentifierType'])
            data['relationType%s' %i] = relationType[i]
            data['relatedID%s' %i] = relatedID[i].encode('ascii', 'xmlcharrefreplace').decode('utf-8', 'ignore')
            data['relationID%s' %i] = relationID[i].encode('ascii', 'xmlcharrefreplace').decode('utf-8', 'ignore')
    
    return data