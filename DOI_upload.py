#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import DOI_B2d
import codecs
import csv
from string import Template


##############################################################
########## GET THE XML FILE FROM THE HTML FORM  ##############
#############################################################
form = cgi.FieldStorage()
message = form['path'].value
#message = form['path'].file.read()

##############################################################
######### RUN THE PROGRAM THAT READ XML METADATA ############
#############################################################

data = DOI_B2d.xml2B2d(message)

##############################################################
##################### FUNCTIONS  ############################
#############################################################

def liste_deroulante(listvalues, realvalue):
    a = ''
    for i in range(0, len(listvalues)):
        if realvalue == listvalues[i][0]:
            listvalues[i][0] = 0
        if listvalues[i][0] != 0:
            a= a + """<option >%s</option>""" %listvalues[i][0]
    a= a + '<option selected="selected">%s</option>' %realvalue
    return a
##############################################################
###################### OPEN FILES  ##########################
#############################################################
file = open('DOI_upload.html')

with open('DataType.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=';')
    datatype = list(reader)
languages = [['en'], ['fr']]
with open('contributorType.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=';')
    contributor_list = list(reader)
with open('license.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=';')
    license_list = list(reader)
with open('relation.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=';')
    relation_list = list(reader)
with open('relatedID.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=';')
    relatedID_list = list(reader)
    
##############################################################
##################### PROCESSING  ############################
#############################################################
temp = Template(file.read())

data['datatype'] = liste_deroulante(datatype, data['datatype'])
data['language'] = liste_deroulante(languages, data['datatype'])
data['authorblock'] =  """ 	<p>
	<div class="form-group row">
		<label for="title" class="col-xs-2 col-form-label">Author name/ Nom de l'auteur*</label>
		<div class="col-xs-9">
			<input class="form-control" type="text" name="authorName0" value="%s" required>
		</div>
	</div>
	</p>
	<p>
	<div class="form-group row">
		<label for="title" class="col-xs-2 col-form-label">Affiliation</label>
		<div class="col-xs-9">
			<input class="form-control" type="text" name="authorAffiliation0" value="%s">
		</div>
	</div>
	</p>
	<p>
	<div class="form-group row">
		<label for="title" class="col-xs-2 col-form-label">ORCID ID / Identifiant ORCID</label>
		<div class="col-xs-9">
			<input class="form-control" type="text" name="authorOrcid0" value="%s">
		</div>
	</div>
	</p> """%(data['authorName0'], data['affiliation0'], data['orcid0'])

if data['authorCounter']>1:
    for i in range(1, data['authorCounter']):
        authorName = data['authorName%d' %i]
        affiliation = data['affiliation%d' %i]
        orcid = data['orcid%d' %i]
        data['authorblock']= data['authorblock'] + """<div class="add-to-del">
        <p>	<div class="form-group row">
        <label for="title" class="col-xs-2 col-form-label">Author name/ Nom de l auteur</label>
        <div class="col-xs-9">
        <input class="form-control" type="text" name="authorName%s" value="%s">
        </div>	</div>	</p>
        <p>	<div class="form-group row">
        <label for="title" class="col-xs-2 col-form-label">Affiliation *</label>
        <div class="col-xs-9">
        <input class="form-control" type="text" name="authorAffiliation%i" value="%s">
        </div>	</div>	</p>
        <p>	<div class="form-group row">
        <label for="title" class="col-xs-2 col-form-label">ORCID ID / Identifiant ORCID</label>
        <div class="col-xs-9">
        <input class="form-control" type="text" name="authorOrcid%d" value="%s">
        </div>	</div>	</p>
  	<p class="delete"><button id="b2" class="btn btn-primary" type="button">-</button></p>
    </div>  </div></div></div>"""%(i, authorName, i, affiliation, i, orcid)
data['add_author'] = """  <div class="dynamic-stuff">
      <div class="form-group row">
	  <label class="col-xs-2 col-form-label" value="test">Add Author</label>
          <p class="add-one"><button id="b1" class="btn btn-primary" type="button">+</button></p>
      </div>
  </div>
</div>
<script type="text/javascript">
var counterAuthor = %s
$('.add-one').click(function(){
  counterAuthor++;
  $('<div class="add-to-del"><p>	<div class="form-group row">	<label for="title" class="col-xs-2 col-form-label">Author name/ Nom de l auteur</label><div class="col-xs-9"><input class="form-control" type="text" name="authorName'+counterAuthor+'" required>	</div>	</div>	</p>	<p>	<div class="form-group row">		<label for="title" class="col-xs-2 col-form-label">Author first name/ Prenom de l auteur*</label>		<div class="col-xs-9">			<input class="form-control" type="text" name="authorFirstname'+counterAuthor+'">	</div></div>  	</p>	<p>	<div class="form-group row">		<label for="title" class="col-xs-2 col-form-label">Affiliation *</label>		<div class="col-xs-9">			<input class="form-control" type="text" name="authorAffiliation'+counterAuthor+'">		</div>	</div>	</p>	<p>	<div class="form-group row">		<label for="title" class="col-xs-2 col-form-label">ORCID ID / Identifiant ORCID</label>		<div class="col-xs-9">			<input class="form-control" type="text" name="authorOrcid'+counterAuthor+'" >		</div>	</div>	</p>      			<p class="delete"><button id="b2" class="btn btn-primary" type="button">-</button></p>    </div>  </div></div></div>').appendTo('.dynamic-stuff').show();
  attach_delete();
});

</script>""" %data['authorCounter']

data['contributorblock'] = ""
if 'contributorCounter' in data:
    for i in range(0, data['contributorCounter']):
        if 'contributorType%s' %i in data:
            contributorType = liste_deroulante(contributor_list, data['contributorType%s' %i])
        else:
            contributorType = ''
        contributorName = data['contributorName%d' %i]
        if 'contributorAffiliation%s' %i in data:
            contributorAffiliation = data['contributorAffiliation%d' %i]
        else:
            contributorAffiliation = ''
        if 'contributorOrcid%d' %i in data:
            contributorOrcid = data['contributorOrcid%d' %i]
        else:
            contributorOrcid = ''
        data['contributorblock'] = data['contributorblock'] + """<div class="add-to-del">
        <p>
        <div class="form-group row">
        <label class="col-xs-2 col-form-label">Contributor type/ Type de contributeur</label>
        <div class="col-xs-9">
        <select class="form-control" name="contributorType%d''">%s
        </select>
        </div></p><p><div class="form-group row">
        </div><label for="title" class="col-xs-2 col-form-label">Contributor name/ Nom du contributeur</label>
        <div class="col-xs-9">
        <input class="form-control" type="text" id=contributorName name="contributorName%d" value="%s">
        </div></div></p>
        <p><div class="form-group row">
        <label class="col-xs-2 col-form-label">Affiliation </label>
        <div class="col-xs-9">
        <input class="form-control" type="text" name="contributorAffiliation%d" value="%s">
        </div>	</div>	</p>
        <p>	<div class="form-group row">
        <label for="title" class="col-xs-2 col-form-label">ORCID ID / Identifiant ORCID</label>
        <div class="col-xs-9">
        <input class="form-control" type="text" name="ContributorOrcid%d" value="%s">
        </div>	</div></p>
        <p class="delete"><button id="b2" class="btn btn-primary" type="button">-</button>
        </p> </div>  </div></div></div>""" %(i,contributorType, i, contributorName, i, contributorAffiliation, i, contributorOrcid)
else:
    data['contributorCounter'] = 0
data['add_contributor'] = """
  <div class="dynamic-stuff3">
      <div class="form-group row">
	  <label class="col-xs-2 col-form-label" value="test">Add Contributor</label>
          <p class="add-one3"><button id="b1" class="btn btn-primary" type="button">+</button></p>
      </div>
  </div>
</div>
<script type="text/javascript">
var counterContributor = %s
$('.add-one3').click(function(){
  counterContributor ++;
  $('<div class="add-to-del"><p><div class="form-group row"><label class="col-xs-2 col-form-label">Contributor type/ Type de contributeur</label><div class="col-xs-9">		<select class="form-control" name="contributorType'+counterContributor+'"><option>ContactPerson</option><option>DataCollector  </option><option>DataCurator   </option><option>DataManager   </option><option>Distributor  </option><option>Editor  </option><option>HostingInstitution  </option><option>Producer  </option><option>ProjectLeader  </option><option>ProjectManager  </option><option>ProjectMember  </option><option>RegistrationAgency  </option><option>RegistrationAuthority  </option><option>RelatedPerson  </option><option>Researcher  </option><option>ResearchGroup  </option><option>RightsHolder  </option><option>Sponsor  </option><option>Supervisor  </option><option>WorkPackageLeader  </option><option>Other</option></select></div></p><p><div class="form-group row"></div><label for="title" class="col-xs-2 col-form-label">Contributor name/ Nom du contributeur</label><div class="col-xs-9"><input class="form-control" type="text" id=contributorName name="contributorName'+counterContributor+'"></div></div></p><p>	<div class="form-group row">		<label class="col-xs-2 col-form-label">Affiliation </label>		<div class="col-xs-9">			<input class="form-control" type="text" name="contributorAffiliation'+counterContributor+'" >		</div>	</div>	</p>	<p>	<div class="form-group row">		<label for="title" class="col-xs-2 col-form-label">ORCID ID / Identifiant ORCID</label>		<div class="col-xs-9">			<input class="form-control" type="text" name="ContributorOrcid'+counterContributor+'" >		</div>	</div>	</p>      			<p class="delete"><button id="b2" class="btn btn-primary" type="button">-</button></p>    </div>  </div></div></div>').appendTo('.dynamic-stuff3').show();
  attach_delete();
});
//Attach functionality to delete buttons
function attach_delete(){
  $('.delete').off();
  $('.delete').click(function(){
    console.log("click");
    $(this).closest('.add-to-del').remove();
  });
}

</script>""" %data['contributorCounter']
if 'license' in data:
    data['license'] = liste_deroulante(license_list, data['license'])

if 'subjectCounter' in data:
    data['subjectblock'] = """
    	<div class="form-group row">
		<label for="title" class="col-xs-2 col-form-label">Subject / Sujet</label>
		<div class="col-xs-9">
			<input class="form-control" type="text" name="subject0" value="%s">
		</div>
	</div>
	</p>""" %data['subject0']
    if data['subjectCounter']>1:
        for i in range(1, data['subjectCounter']):
             data['subjectblock'] = data['subjectblock'] + """<div class="add-to-del">            <div class="form-group row">
            <label for="title" class="col-xs-2 col-form-label">Subject / Sujet</label>            <div class="col-xs-9">
            <input class="col-xs-9 col-form-label" type="text" name="subject%d" value="%s">            <p class="delete">
            <button class="btn btn-primary" type="button">-</button></p></div></div>""" %(i, data['subject%d' %i])
else:
    data['subjectCounter'] = 0
    data['subjectblock'] = """	<div class="form-group row">
		<label for="title" class="col-xs-2 col-form-label">Subject / Sujet</label>
		<div class="col-xs-9">
			<input class="form-control" type="text" name="subject0">
		</div>
	</div>
	</p>"""
data['add_subject'] = """ <div class="dynamic-stuff4">
      <div class="form-group row">
	  <label class="col-xs-2 col-form-label" value="test">Add subject</label>
          <p class="add-one4"><button id="b2" class="btn btn-primary" type="button">+</button></p>
      </div>
  </div>
</div>
<script type="text/javascript">
var counterSubject = %s
$('.add-one4').click(function(){
  counterSubject ++;
  $('<div class="add-to-del"><div class="form-group row"><label for="title" class="col-xs-2 col-form-label">Subject / Sujet</label><div class="col-xs-9"><input class="col-xs-9 col-form-label" type="text" name="subject'+counterSubject+'"><p class="delete"><button class="btn btn-primary" type="button">-</button></p></div></div>').appendTo('.dynamic-stuff4').show();
  attach_delete();
});
</script>
	</p>""" %data['subjectCounter']
 

data['relationblock'] = ""
if 'relationCounter' in data:
    for i in range(0, data['relationCounter']):
        if 'relationType%s' %i in data:
            relationType = liste_deroulante(relation_list, data['relationType%s' %i])
        else:
            relationType = ''
        if 'relatedID%s' %i in data:
            relatedID = liste_deroulante(relatedID_list, data['relatedID%s' %i])
        else:
            relatedID = ''
        relationID = data['relationID%d' %i]
        data['relationblock'] = data['relationblock'] + """<div class="add-to-del">
        <p>	<div class="form-group row">
        <label for="datatype" class="col-xs-2 col-form-label">Relation type </label>
        <div class="col-xs-9">
        <select class="form-control" name="relationType%d">
        %s</select>		</div>	</div>	</p>
        <p>	<div class="form-group row">
        <label class="col-xs-2 col-form-label">Related Identifier type </label>
        <div class="col-xs-9">
        <select class="form-control" name="relationIDtype%d">%s</select>
        </div>	</div>	</p>	</p>
        <div class="form-group row">
        <label class="col-xs-2 col-form-label">Identifier</label>
        <div class="col-xs-9">
        <input class="form-control" type="text" name="relatedID%d" value="%s">
        </div>	</div>	</p><p class="delete">
        <button class="btn btn-primary" type="button">-</button>
        </p></div>""" %(i,relationType, i, relatedID, i, relationID)
else:
     data['relationCounter'] = 0   

data['add_relation'] = """    <div class="dynamic-stuff5">
      <div class="form-group row">
	  <label class="col-xs-2 col-form-label" value="test">Add related resources</label>
          <p class="add-one5"><button id="b2" class="btn btn-primary" type="button">+</button></p>
      </div>
  </div>
</div>
<script type="text/javascript">
var counterResource = %d
$('.add-one5').click(function(){
  counterResource ++;
  $('<div class="add-to-del">	<p>	<div class="form-group row">		<label for="datatype" class="col-xs-2 col-form-label">Relation type </label>		<div class="col-xs-9">		<select class="form-control" name="relationType'+counterResource+'"><option>IsCitedBy  </option><option>Cites  </option><option>IsSupplementTo  </option><option>IsSupplementedBy  </option><option>IsContinuedBy  </option><option>Continues  </option><option>HasMetadata  </option><option>IsMetadataFor  </option><option>IsNewVersionOf  </option><option>IsPreviousVersionOf  </option><option>IsPartOf  </option><option>HasPart  </option><option>IsReferencedBy  </option><option>References  </option><option>IsDocumentedBy  </option><option>Documents  </option><option>IsCompiledBy  </option><option>Compiles  </option><option>IsVariantFormOf  </option><option>IsOriginalFormOf  </option><option>IsIdenticalTo  </option><option>IsReviewedBy  </option><option>Reviews  </option><option>IsDerivedFrom  </option><option>IsSourceOf</option>	</select>		</div>	</div>	</p>	<p>	<div class="form-group row">		<label class="col-xs-2 col-form-label">Related Identifier type </label>		<div class="col-xs-9">		<select class="form-control" name="relationIDtype'+counterResource+'"><option>ARK  </option><option>arXiv  </option><option>bibcode  </option><option>DOI  </option><option>EAN13  </option><option>EISSN  </option><option>Handle  </option><option>IGSN  </option><option>ISBN  </option><option>ISSN  </option><option>ISTC  </option><option>LISSN  </option><option>LSID  </option><option>PMID  </option><option>PURL  </option><option>UPC  </option><option>URL  </option><option>URN</option>		</select>		</div>	</div>	</p>	</p>	<div class="form-group row">		<label class="col-xs-2 col-form-label">Identifier</label>		<div class="col-xs-9">			<input class="form-control" type="text" name="relatedID'+counterResource+'">		</div>	</div>	</p><p class="delete"><button class="btn btn-primary" type="button">-</button></p></div>').appendTo('.dynamic-stuff5').show();
  attach_delete();
});
</script>
""" %data['relationCounter']


#toreplace = {a.keys: a.values.encode('ascii', 'xmlcharrefreplace').decode('utf-8', 'ignore') for a in form.keys()}
print("Content-type: text/html; charset=utf-8\n")
#print(message)
print(temp.substitute(data))
#print(data)