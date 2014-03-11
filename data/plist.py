# Copyright 2003 Kevin Reid  <kpreid@mac.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""Converts Mac OS X property lists to and from Python structures.

Supports types str, unicode, int, float, list, tuple, and dict.

str is mapped to <data/>, and unicode is mapped to <string/>.
"""

__version__ = "1.1"
__all__ = ["parsePlistFile", "plistToStructure", "plistNodeToStructure", "toPlist"]

import xml.dom.minidom
import base64

def parsePlistFile(filename):
  """Convert a property list file to a Python object, given the filename."""
  return plistToStructure(xml.dom.minidom.parse(filename))

def parsePlist(plistString):
  """Convert a property list to a Python object."""
  return plistToStructure(xml.dom.minidom.parseString(plistString))

def plistToStructure(domDocument):
  """Convert a property list to a Python object, given an XML DOM document."""
  node = domDocument.documentElement
  node.normalize()
  return plistNodeToStructure(node)

def plistNodeToStructure(node):
  """Convert a property list to a Python object, given an XML DOM element node."""
  if node.nodeType != node.ELEMENT_NODE:
    raise ValueError()
  kids = filter(lambda kid:kid.nodeType == kid.ELEMENT_NODE, node.childNodes)
  if node.localName == 'plist':
    return plistNodeToStructure(kids[0])
  elif node.localName == 'string':
    if len(node.childNodes):
      return node.childNodes[0].data
    else:
      return ""
  elif node.localName == 'integer':
    if len(node.childNodes):
      return int(node.childNodes[0].data)
    else:
      return 0
  elif node.localName == 'real':
    if len(node.childNodes):
      return float(node.childNodes[0].data)
    else:
      return 0.0
  elif node.localName == 'array':
    return map(plistNodeToStructure, kids)
  elif node.localName == 'data':
    return base64.decodestring(node.childNodes[0].data)
  elif node.localName == 'dict':
    lastkey = None
    result = {}
    for kid in kids:
      if kid.localName == 'key':
        lastkey = kid.childNodes[0].data
      else:
        result[lastkey] = plistNodeToStructure(kid)
    return result
  else:
    return "Unrecognized node: " + node.localName

def _xmlesc(s):
  return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;")

def toPlistElement(value):
  """Convert a Python object of a supported type to a fragment of a property list."""
  if isinstance(value, unicode):
    return u"<string>" + _xmlesc(value) + u"</string>\n"
  elif isinstance(value,  str):
    return u"<data>" + _xmlesc(base64.encodestring(value)) + u"</data>\n"
  elif isinstance(value, int):
    return u"<integer>" + _xmlesc(repr(value)) + u"</integer>\n"
  elif isinstance(value, float):
    return u"<real>" + _xmlesc(repr(value)) + u"</real>\n"
  elif isinstance(value, list) or isinstance(value, tuple):
    return u"<array>\n" + u"".join([toPlistElement(sub) for sub in value])  + u"</array>\n"
  elif isinstance(value, dict):
    return u"<dict>\n" + u"".join([u"<key>" + _xmlesc(str(key)) + u"</key>\n" + toPlistElement(value[key]) for key in value]) + u"</dict>\n"
  else:
    raise TypeError("cannot encode value %s of type %s in property list" % (value, type(value)))

def toPlist(value):
  """Convert a Python object of a supported type to a property list."""
  return (
    u'<?xml version="1.0" encoding="UTF-8"?>\n' +
    u'<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n' +
    u'<plist version="1.0">\n' +
    toPlistElement(value) +
    u'</plist>\n'
  ).encode("UTF-8")

# afterthought, incomplete
if __name__ == "__main__":
  def _roundtrip(x):
    assert x == parsePlist(toPlist(x))
  _roundtrip(241)
  _roundtrip(43.5)
  _roundtrip("abc")
  _roundtrip("&a<b>c\"'")
  _roundtrip(u"def")
  _roundtrip(u"d><e'f")
  _roundtrip([1, "2", 3.0])
  _roundtrip({u"a":1, u"b":"2", u"3":3.0})
  print "Tests OK"
