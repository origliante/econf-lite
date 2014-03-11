import libxml2
import libxslt

styledoc = libxml2.parseFile("hosts.xsl")
style = libxslt.parseStylesheetDoc(styledoc)
doc = libxml2.parseFile("config.xml")
result = style.applyStylesheet(doc, None)
style.saveResultToFilename("foo", result, 0)
style.freeStylesheet()
doc.freeDoc()
print result
result.freeDoc()
