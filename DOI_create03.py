#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import DOI_XML2
from datetime import datetime

##############################################################
########## GET THE VALUE FROM THE HTML FORM  ################
#############################################################

form = cgi.FieldStorage()
data = {a:form.getvalue(a) for a in form.keys()}

##############################################################
########## TRANSFORM VALUE INTO XML METADATA  ################
#############################################################
DOI_XML2.xml(data)

##############################################################
################ DISPLAY RESULTS  ##########################
#############################################################
print("Content-type: text/html")
print("""
<html lang="en">
 <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">

<title>Metadata DOI</title>
	<link href="css/bootstrap-combined.min.css" rel="stylesheet">
	<link rel="stylesheet" type="text/css" media="screen"
	 href="css/bootstrap-datetimepicker.min.css">
	<link href="css/bootstrap.min.css" rel="stylesheet">
	<script type="text/javascript"
	 src="js/jquery.min.js">
	</script> 
	<script type="text/javascript"
	 src="js/bootstrap.min.js">
	</script>
	<script type="text/javascript"
	 src="js/bootstrap-datetimepicker.min.js">
	</script>
</head>

<body>
<div class="container">
	<nav class="navbar navbar-default navbar-fixed-top">
		<div class="container-fluid">
			<a class="navbar-brand" href="https://cdgp.u-strasbg.fr/">
				<div class="form-group row">
					<div class="col-xs-2"><img src="img/logo_cdgp.png" width="100" height="100"></div>
				Centre de Donnees de Geothermie Profonde
				</div>
			</a>
		</div>
		<div id="navbar" class="collapse navbar-collapse">
			<ul class="nav navbar-nav">
				<li class="active" href='index3.py'><a href="index3.py">Metadata DOI</a></li>
				<li><a href="upload.html">Uploading metadata</a></li>
				<li href='excel.html'><a href="excel.html">Excel tools</a></li>
				<li><a href="about.html">About and Procedures</a></li>
				<li><a href="contact.html">Contact</a></li>
			</ul>
		</div>
	</nav>
</div>

<div class="page-header">
        <h1><center>Succeed!! Here are the value you entered </center></h1>
        <h2><center> Please check the value. XML available below</center></h2>
<fieldset>""")
print('<h4><b>DOI </b>: %s </h4>'%data['doi'])
print('<h4><b>URL</b>: %s </h4>'%data['url'])
print('<h4><b>Title / Titre</b>: %s </h4>'%data['title'].encode('utf-8'))
print('</fieldset><fieldset>')
print("<h4><b>Author name/ Nom de l'auteur</b>: %s </h4>" %data['authorName0'].encode('utf-8'))
print("<h4><b>Publisher / editeur</b>: %s </h4>" %data['publisher0'].encode('utf-8'))
print("<h4><b>Publication year/ Annee de publication</b>: %s </h4>" %data['year'])
print("""
    </fieldset>
    <fieldset>
	<p>
	<h2> XML</h2>
	</p>
 <h3>Click on the image logo to download the XML:</h3>""")
print(' <a href="File/XML_temp.xml" download="%s.xml"><center>' % data['title'])
print("""<img src="File/XML.jpg" width="104"/></center>
</a>
<p><b>Note:</b> The download attribute is not supported in Edge version 12, IE, Safari or Opera version 12 (and earlier).</p>
</fieldset>""")

print("""
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script>window.jQuery || document.write('<script src="../../assets/js/vendor/jquery.min.js"><\/script>')</script>

  </body>
</html>""")
