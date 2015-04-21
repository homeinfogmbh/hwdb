# ./terminallib.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:e0f2b2b6088681bd91db874b9eaa9b60ccb9bc46
# Generated 2015-04-20 12:12:56.713788 by PyXB version 1.2.5-DEV using Python 3.4.3.final.0
# Namespace http://xml.homeinfo.de/schema/terminallib

from __future__ import unicode_literals
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys
import pyxb.utils.six as _six

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:d0994312-e745-11e4-ab38-7427eaa9df7d')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.5-DEV'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://xml.homeinfo.de/schema/terminallib', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.

    @param xml_text An XML document.  This should be data (Python 2
    str or Python 3 bytes), or a text (Python 2 unicode or Python 3
    str) in the L{pyxb._InputEncoding} encoding.

    @keyword default_namespace The L{pyxb.Namespace} instance to use as the
    default namespace where there is no default namespace in scope.
    If unspecified or C{None}, the namespace of the module containing
    this function will be used.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement, default_namespace=default_namespace)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# Atomic simple type: {http://xml.homeinfo.de/schema/terminallib}TerminalStatus
class TerminalStatus (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """
                The status of the terminal
            """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TerminalStatus')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 305, 4)
    _Documentation = '\n                The status of the terminal\n            '
TerminalStatus._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=TerminalStatus, enum_prefix=None)
TerminalStatus.UP = TerminalStatus._CF_enumeration.addEnumeration(unicode_value='UP', tag='UP')
TerminalStatus.DOWN = TerminalStatus._CF_enumeration.addEnumeration(unicode_value='DOWN', tag='DOWN')
TerminalStatus._InitializeFacetMap(TerminalStatus._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'TerminalStatus', TerminalStatus)

# Atomic simple type: {http://xml.homeinfo.de/schema/terminallib}IPv4Address
class IPv4Address (pyxb.binding.datatypes.string):

    """
                An IPv4 address
            """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'IPv4Address')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 319, 4)
    _Documentation = '\n                An IPv4 address\n            '
IPv4Address._CF_pattern = pyxb.binding.facets.CF_pattern()
IPv4Address._CF_pattern.addPattern(pattern='(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])\\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])\\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])\\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])')
IPv4Address._InitializeFacetMap(IPv4Address._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'IPv4Address', IPv4Address)

# Complex type {http://xml.homeinfo.de/schema/terminallib}TerminalLibrary with content type ELEMENT_ONLY
class TerminalLibrary (pyxb.binding.basis.complexTypeDefinition):
    """
                A terminal web API solution by HOMEINFO Digitale Informationssysteme GmbH
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TerminalLibrary')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 12, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element terminal uses Python identifier terminal
    __terminal = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'terminal'), 'terminal', '__httpxml_homeinfo_deschematerminallib_TerminalLibrary_terminal', True, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 19, 12), )

    
    terminal = property(__terminal.value, __terminal.set, None, None)

    
    # Element terminal_detail uses Python identifier terminal_detail
    __terminal_detail = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'terminal_detail'), 'terminal_detail', '__httpxml_homeinfo_deschematerminallib_TerminalLibrary_terminal_detail', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 20, 12), )

    
    terminal_detail = property(__terminal_detail.value, __terminal_detail.set, None, None)

    
    # Element class uses Python identifier class_
    __class = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'class'), 'class_', '__httpxml_homeinfo_deschematerminallib_TerminalLibrary_class', True, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 21, 12), )

    
    class_ = property(__class.value, __class.set, None, None)

    
    # Element domain uses Python identifier domain
    __domain = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'domain'), 'domain', '__httpxml_homeinfo_deschematerminallib_TerminalLibrary_domain', True, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 22, 12), )

    
    domain = property(__domain.value, __domain.set, None, None)

    
    # Element setup_operator uses Python identifier setup_operator
    __setup_operator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'setup_operator'), 'setup_operator', '__httpxml_homeinfo_deschematerminallib_TerminalLibrary_setup_operator', True, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 23, 12), )

    
    setup_operator = property(__setup_operator.value, __setup_operator.set, None, None)

    
    # Element administrator uses Python identifier administrator
    __administrator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'administrator'), 'administrator', '__httpxml_homeinfo_deschematerminallib_TerminalLibrary_administrator', True, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 24, 12), )

    
    administrator = property(__administrator.value, __administrator.set, None, None)

    _ElementMap.update({
        __terminal.name() : __terminal,
        __terminal_detail.name() : __terminal_detail,
        __class.name() : __class,
        __domain.name() : __domain,
        __setup_operator.name() : __setup_operator,
        __administrator.name() : __administrator
    })
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', 'TerminalLibrary', TerminalLibrary)


# Complex type {http://xml.homeinfo.de/schema/terminallib}Customer with content type ELEMENT_ONLY
class Customer (pyxb.binding.basis.complexTypeDefinition):
    """
                Terminal data for a certain customer
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Customer')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 30, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element terminal uses Python identifier terminal
    __terminal = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'terminal'), 'terminal', '__httpxml_homeinfo_deschematerminallib_Customer_terminal', True, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 37, 12), )

    
    terminal = property(__terminal.value, __terminal.set, None, None)

    
    # Attribute cid uses Python identifier cid
    __cid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'cid'), 'cid', '__httpxml_homeinfo_deschematerminallib_Customer_cid', pyxb.binding.datatypes.integer, required=True)
    __cid._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 39, 8)
    __cid._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 39, 8)
    
    cid = property(__cid.value, __cid.set, None, '\n                    The customer identifier\n                ')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__httpxml_homeinfo_deschematerminallib_Customer_name', pyxb.binding.datatypes.string)
    __name._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 46, 8)
    __name._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 46, 8)
    
    name = property(__name.value, __name.set, None, "\n                    The customer's full name\n                ")

    _ElementMap.update({
        __terminal.name() : __terminal
    })
    _AttributeMap.update({
        __cid.name() : __cid,
        __name.name() : __name
    })
Namespace.addCategoryObject('typeBinding', 'Customer', Customer)


# Complex type {http://xml.homeinfo.de/schema/terminallib}Terminal with content type ELEMENT_ONLY
class Terminal (pyxb.binding.basis.complexTypeDefinition):
    """
                Terminal information
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Terminal')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 57, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element cls uses Python identifier cls
    __cls = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'cls'), 'cls', '__httpxml_homeinfo_deschematerminallib_Terminal_cls', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 64, 12), )

    
    cls = property(__cls.value, __cls.set, None, None)

    
    # Element domain uses Python identifier domain
    __domain = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'domain'), 'domain', '__httpxml_homeinfo_deschematerminallib_Terminal_domain', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 65, 12), )

    
    domain = property(__domain.value, __domain.set, None, None)

    
    # Element ipv4addr uses Python identifier ipv4addr
    __ipv4addr = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ipv4addr'), 'ipv4addr', '__httpxml_homeinfo_deschematerminallib_Terminal_ipv4addr', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 66, 12), )

    
    ipv4addr = property(__ipv4addr.value, __ipv4addr.set, None, None)

    
    # Element virtual_display uses Python identifier virtual_display
    __virtual_display = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'virtual_display'), 'virtual_display', '__httpxml_homeinfo_deschematerminallib_Terminal_virtual_display', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 67, 12), )

    
    virtual_display = property(__virtual_display.value, __virtual_display.set, None, None)

    
    # Element location uses Python identifier location
    __location = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'location'), 'location', '__httpxml_homeinfo_deschematerminallib_Terminal_location', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 68, 12), )

    
    location = property(__location.value, __location.set, None, None)

    
    # Attribute tid uses Python identifier tid
    __tid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'tid'), 'tid', '__httpxml_homeinfo_deschematerminallib_Terminal_tid', pyxb.binding.datatypes.integer, required=True)
    __tid._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 70, 8)
    __tid._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 70, 8)
    
    tid = property(__tid.value, __tid.set, None, '\n                    The terminal identifier\n                ')

    
    # Attribute cid uses Python identifier cid
    __cid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'cid'), 'cid', '__httpxml_homeinfo_deschematerminallib_Terminal_cid', pyxb.binding.datatypes.integer, required=True)
    __cid._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 77, 8)
    __cid._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 77, 8)
    
    cid = property(__cid.value, __cid.set, None, '\n                    The customer identifier\n                ')

    _ElementMap.update({
        __cls.name() : __cls,
        __domain.name() : __domain,
        __ipv4addr.name() : __ipv4addr,
        __virtual_display.name() : __virtual_display,
        __location.name() : __location
    })
    _AttributeMap.update({
        __tid.name() : __tid,
        __cid.name() : __cid
    })
Namespace.addCategoryObject('typeBinding', 'Terminal', Terminal)


# Complex type {http://xml.homeinfo.de/schema/terminallib}Terminals with content type ELEMENT_ONLY
class Terminals (pyxb.binding.basis.complexTypeDefinition):
    """
                A list of Terminals
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Terminals')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 110, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element terminal uses Python identifier terminal
    __terminal = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'terminal'), 'terminal', '__httpxml_homeinfo_deschematerminallib_Terminals_terminal', True, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 117, 12), )

    
    terminal = property(__terminal.value, __terminal.set, None, None)

    _ElementMap.update({
        __terminal.name() : __terminal
    })
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', 'Terminals', Terminals)


# Complex type {http://xml.homeinfo.de/schema/terminallib}Class with content type SIMPLE
class Class (pyxb.binding.basis.complexTypeDefinition):
    """
                Terminal class
            """
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Class')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 123, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute touch uses Python identifier touch
    __touch = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'touch'), 'touch', '__httpxml_homeinfo_deschematerminallib_Class_touch', pyxb.binding.datatypes.boolean, required=True)
    __touch._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 131, 16)
    __touch._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 131, 16)
    
    touch = property(__touch.value, __touch.set, None, '\n                            Flag whether it is a class with touch screen\n                        ')

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpxml_homeinfo_deschematerminallib_Class_id', pyxb.binding.datatypes.integer, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 138, 16)
    __id._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 138, 16)
    
    id = property(__id.value, __id.set, None, '\n                            The unique ID of the class\n                        ')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __touch.name() : __touch,
        __id.name() : __id
    })
Namespace.addCategoryObject('typeBinding', 'Class', Class)


# Complex type {http://xml.homeinfo.de/schema/terminallib}Domain with content type SIMPLE
class Domain (pyxb.binding.basis.complexTypeDefinition):
    """
                A terminal's domain
            """
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Domain')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 151, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpxml_homeinfo_deschematerminallib_Domain_id', pyxb.binding.datatypes.integer, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 159, 16)
    __id._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 159, 16)
    
    id = property(__id.value, __id.set, None, '\n                            The unique ID of the domain\n                        ')

    
    # Attribute mimetype uses Python identifier mimetype
    __mimetype = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'mimetype'), 'mimetype', '__httpxml_homeinfo_deschematerminallib_Domain_mimetype', pyxb.binding.datatypes.string, required=True)
    __mimetype._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 166, 16)
    __mimetype._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 166, 16)
    
    mimetype = property(__mimetype.value, __mimetype.set, None, "\n                            The screenshot picture's mime type\n                        ")

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __id.name() : __id,
        __mimetype.name() : __mimetype
    })
Namespace.addCategoryObject('typeBinding', 'Domain', Domain)


# Complex type {http://xml.homeinfo.de/schema/terminallib}Address with content type ELEMENT_ONLY
class Address (pyxb.binding.basis.complexTypeDefinition):
    """
                Terminal address
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Address')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 179, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element street uses Python identifier street
    __street = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'street'), 'street', '__httpxml_homeinfo_deschematerminallib_Address_street', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 186, 12), )

    
    street = property(__street.value, __street.set, None, None)

    
    # Element house_number uses Python identifier house_number
    __house_number = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'house_number'), 'house_number', '__httpxml_homeinfo_deschematerminallib_Address_house_number', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 187, 12), )

    
    house_number = property(__house_number.value, __house_number.set, None, None)

    
    # Element city uses Python identifier city
    __city = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'city'), 'city', '__httpxml_homeinfo_deschematerminallib_Address_city', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 188, 12), )

    
    city = property(__city.value, __city.set, None, None)

    
    # Element zip_code uses Python identifier zip_code
    __zip_code = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'zip_code'), 'zip_code', '__httpxml_homeinfo_deschematerminallib_Address_zip_code', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 189, 12), )

    
    zip_code = property(__zip_code.value, __zip_code.set, None, None)

    _ElementMap.update({
        __street.name() : __street,
        __house_number.name() : __house_number,
        __city.name() : __city,
        __zip_code.name() : __zip_code
    })
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', 'Address', Address)


# Complex type {http://xml.homeinfo.de/schema/terminallib}Screenshot with content type SIMPLE
class Screenshot (pyxb.binding.basis.complexTypeDefinition):
    """
                A screen shot of a terminal
            """
    _TypeDefinition = pyxb.binding.datatypes.base64Binary
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Screenshot')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 195, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.base64Binary
    
    # Attribute timestamp uses Python identifier timestamp
    __timestamp = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'timestamp'), 'timestamp', '__httpxml_homeinfo_deschematerminallib_Screenshot_timestamp', pyxb.binding.datatypes.dateTime, required=True)
    __timestamp._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 203, 16)
    __timestamp._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 203, 16)
    
    timestamp = property(__timestamp.value, __timestamp.set, None, '\n                            The time, when the screenshot was taken\n                        ')

    
    # Attribute mimetype uses Python identifier mimetype
    __mimetype = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'mimetype'), 'mimetype', '__httpxml_homeinfo_deschematerminallib_Screenshot_mimetype', pyxb.binding.datatypes.string, required=True)
    __mimetype._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 210, 16)
    __mimetype._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 210, 16)
    
    mimetype = property(__mimetype.value, __mimetype.set, None, "\n                            The screenshot picture's mime type\n                        ")

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __timestamp.name() : __timestamp,
        __mimetype.name() : __mimetype
    })
Namespace.addCategoryObject('typeBinding', 'Screenshot', Screenshot)


# Complex type {http://xml.homeinfo.de/schema/terminallib}TouchEvent with content type SIMPLE
class TouchEvent (pyxb.binding.basis.complexTypeDefinition):
    """
                Touch input event
            """
    _TypeDefinition = pyxb.binding.datatypes.dateTime
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TouchEvent')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 223, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.dateTime
    
    # Attribute x uses Python identifier x
    __x = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'x'), 'x', '__httpxml_homeinfo_deschematerminallib_TouchEvent_x', pyxb.binding.datatypes.integer, required=True)
    __x._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 231, 16)
    __x._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 231, 16)
    
    x = property(__x.value, __x.set, None, '\n                            The x-coordinate of the touch event\n                        ')

    
    # Attribute y uses Python identifier y
    __y = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'y'), 'y', '__httpxml_homeinfo_deschematerminallib_TouchEvent_y', pyxb.binding.datatypes.integer, required=True)
    __y._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 238, 16)
    __y._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 238, 16)
    
    y = property(__y.value, __y.set, None, '\n                            The y-coordinate of the touch event\n                        ')

    
    # Attribute duration uses Python identifier duration
    __duration = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'duration'), 'duration', '__httpxml_homeinfo_deschematerminallib_TouchEvent_duration', pyxb.binding.datatypes.integer)
    __duration._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 245, 16)
    __duration._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 245, 16)
    
    duration = property(__duration.value, __duration.set, None, '\n                            The duration of the touch event\n                        ')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __x.name() : __x,
        __y.name() : __y,
        __duration.name() : __duration
    })
Namespace.addCategoryObject('typeBinding', 'TouchEvent', TouchEvent)


# Complex type {http://xml.homeinfo.de/schema/terminallib}Message with content type ELEMENT_ONLY
class Message (pyxb.binding.basis.complexTypeDefinition):
    """
                Messages
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Message')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 258, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element text uses Python identifier text
    __text = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'text'), 'text', '__httpxml_homeinfo_deschematerminallib_Message_text', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 265, 12), )

    
    text = property(__text.value, __text.set, None, "\n                        The messages' body or content\n                    ")

    
    # Attribute code uses Python identifier code
    __code = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'code'), 'code', '__httpxml_homeinfo_deschematerminallib_Message_code', pyxb.binding.datatypes.integer, required=True)
    __code._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 273, 8)
    __code._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 273, 8)
    
    code = property(__code.value, __code.set, None, '\n                    A unique message code\n                ')

    _ElementMap.update({
        __text.name() : __text
    })
    _AttributeMap.update({
        __code.name() : __code
    })
Namespace.addCategoryObject('typeBinding', 'Message', Message)


# Complex type {http://xml.homeinfo.de/schema/terminallib}Text with content type SIMPLE
class Text (pyxb.binding.basis.complexTypeDefinition):
    """
                Localized text string
            """
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Text')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 284, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute lang uses Python identifier lang
    __lang = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'lang'), 'lang', '__httpxml_homeinfo_deschematerminallib_Text_lang', pyxb.binding.datatypes.string, required=True)
    __lang._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 292, 16)
    __lang._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 292, 16)
    
    lang = property(__lang.value, __lang.set, None, '\n                            The language of the text\n                        ')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __lang.name() : __lang
    })
Namespace.addCategoryObject('typeBinding', 'Text', Text)


# Complex type {http://xml.homeinfo.de/schema/terminallib}SetupOperator with content type SIMPLE
class SetupOperator (pyxb.binding.basis.complexTypeDefinition):
    """
                An operator that is allowed to setup terminals
            """
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'SetupOperator')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 334, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpxml_homeinfo_deschematerminallib_SetupOperator_id', pyxb.binding.datatypes.integer, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 342, 16)
    __id._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 342, 16)
    
    id = property(__id.value, __id.set, None, '\n                            The ID of the operator\n                        ')

    
    # Attribute annotation uses Python identifier annotation
    __annotation = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'annotation'), 'annotation', '__httpxml_homeinfo_deschematerminallib_SetupOperator_annotation', pyxb.binding.datatypes.string)
    __annotation._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 349, 16)
    __annotation._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 349, 16)
    
    annotation = property(__annotation.value, __annotation.set, None, '\n                            An optional annotation\n                        ')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __id.name() : __id,
        __annotation.name() : __annotation
    })
Namespace.addCategoryObject('typeBinding', 'SetupOperator', SetupOperator)


# Complex type {http://xml.homeinfo.de/schema/terminallib}Administrator with content type SIMPLE
class Administrator (pyxb.binding.basis.complexTypeDefinition):
    """
                An administrator that is allowed to manage terminals
            """
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Administrator')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 362, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpxml_homeinfo_deschematerminallib_Administrator_id', pyxb.binding.datatypes.integer, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 370, 16)
    __id._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 370, 16)
    
    id = property(__id.value, __id.set, None, '\n                            The ID of the administrator\n                        ')

    
    # Attribute annotation uses Python identifier annotation
    __annotation = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'annotation'), 'annotation', '__httpxml_homeinfo_deschematerminallib_Administrator_annotation', pyxb.binding.datatypes.string)
    __annotation._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 377, 16)
    __annotation._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 377, 16)
    
    annotation = property(__annotation.value, __annotation.set, None, '\n                            An optional annotation\n                        ')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __id.name() : __id,
        __annotation.name() : __annotation
    })
Namespace.addCategoryObject('typeBinding', 'Administrator', Administrator)


# Complex type {http://xml.homeinfo.de/schema/terminallib}TerminalDetail with content type ELEMENT_ONLY
class TerminalDetail (Terminal):
    """
                More detailed terminal information
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TerminalDetail')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 88, 4)
    _ElementMap = Terminal._ElementMap.copy()
    _AttributeMap = Terminal._AttributeMap.copy()
    # Base type is Terminal
    
    # Element cls (cls) inherited from {http://xml.homeinfo.de/schema/terminallib}Terminal
    
    # Element domain (domain) inherited from {http://xml.homeinfo.de/schema/terminallib}Terminal
    
    # Element ipv4addr (ipv4addr) inherited from {http://xml.homeinfo.de/schema/terminallib}Terminal
    
    # Element virtual_display (virtual_display) inherited from {http://xml.homeinfo.de/schema/terminallib}Terminal
    
    # Element location (location) inherited from {http://xml.homeinfo.de/schema/terminallib}Terminal
    
    # Element status uses Python identifier status
    __status = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'status'), 'status', '__httpxml_homeinfo_deschematerminallib_TerminalDetail_status', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 97, 20), )

    
    status = property(__status.value, __status.set, None, None)

    
    # Element uptime uses Python identifier uptime
    __uptime = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'uptime'), 'uptime', '__httpxml_homeinfo_deschematerminallib_TerminalDetail_uptime', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 98, 20), )

    
    uptime = property(__uptime.value, __uptime.set, None, None)

    
    # Element screenshot uses Python identifier screenshot
    __screenshot = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'screenshot'), 'screenshot', '__httpxml_homeinfo_deschematerminallib_TerminalDetail_screenshot', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 99, 20), )

    
    screenshot = property(__screenshot.value, __screenshot.set, None, None)

    
    # Element touch_event uses Python identifier touch_event
    __touch_event = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'touch_event'), 'touch_event', '__httpxml_homeinfo_deschematerminallib_TerminalDetail_touch_event', True, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 100, 20), )

    
    touch_event = property(__touch_event.value, __touch_event.set, None, None)

    
    # Element setup_operator uses Python identifier setup_operator
    __setup_operator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'setup_operator'), 'setup_operator', '__httpxml_homeinfo_deschematerminallib_TerminalDetail_setup_operator', True, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 101, 20), )

    
    setup_operator = property(__setup_operator.value, __setup_operator.set, None, None)

    
    # Element administrator uses Python identifier administrator
    __administrator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'administrator'), 'administrator', '__httpxml_homeinfo_deschematerminallib_TerminalDetail_administrator', True, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 102, 20), )

    
    administrator = property(__administrator.value, __administrator.set, None, None)

    
    # Attribute tid inherited from {http://xml.homeinfo.de/schema/terminallib}Terminal
    
    # Attribute cid inherited from {http://xml.homeinfo.de/schema/terminallib}Terminal
    _ElementMap.update({
        __status.name() : __status,
        __uptime.name() : __uptime,
        __screenshot.name() : __screenshot,
        __touch_event.name() : __touch_event,
        __setup_operator.name() : __setup_operator,
        __administrator.name() : __administrator
    })
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', 'TerminalDetail', TerminalDetail)


terminallib = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'terminallib'), TerminalLibrary, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 8, 4))
Namespace.addCategoryObject('elementBinding', terminallib.name().localName(), terminallib)



TerminalLibrary._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'terminal'), Terminal, scope=TerminalLibrary, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 19, 12)))

TerminalLibrary._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'terminal_detail'), TerminalDetail, scope=TerminalLibrary, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 20, 12)))

TerminalLibrary._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'class'), Class, scope=TerminalLibrary, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 21, 12)))

TerminalLibrary._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'domain'), Domain, scope=TerminalLibrary, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 22, 12)))

TerminalLibrary._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'setup_operator'), SetupOperator, scope=TerminalLibrary, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 23, 12)))

TerminalLibrary._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'administrator'), Administrator, scope=TerminalLibrary, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 24, 12)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 19, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 21, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 22, 12))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 23, 12))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 24, 12))
    counters.add(cc_4)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(TerminalLibrary._UseForTag(pyxb.namespace.ExpandedName(None, 'terminal')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 19, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(TerminalLibrary._UseForTag(pyxb.namespace.ExpandedName(None, 'terminal_detail')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 20, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(TerminalLibrary._UseForTag(pyxb.namespace.ExpandedName(None, 'class')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 21, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(TerminalLibrary._UseForTag(pyxb.namespace.ExpandedName(None, 'domain')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 22, 12))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(TerminalLibrary._UseForTag(pyxb.namespace.ExpandedName(None, 'setup_operator')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 23, 12))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(TerminalLibrary._UseForTag(pyxb.namespace.ExpandedName(None, 'administrator')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 24, 12))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
TerminalLibrary._Automaton = _BuildAutomaton()




Customer._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'terminal'), Terminal, scope=Customer, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 37, 12)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Customer._UseForTag(pyxb.namespace.ExpandedName(None, 'terminal')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 37, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Customer._Automaton = _BuildAutomaton_()




Terminal._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'cls'), Class, scope=Terminal, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 64, 12)))

Terminal._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'domain'), Domain, scope=Terminal, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 65, 12)))

Terminal._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ipv4addr'), IPv4Address, scope=Terminal, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 66, 12)))

Terminal._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'virtual_display'), pyxb.binding.datatypes.integer, scope=Terminal, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 67, 12)))

Terminal._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'location'), Address, scope=Terminal, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 68, 12)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 67, 12))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Terminal._UseForTag(pyxb.namespace.ExpandedName(None, 'cls')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 64, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Terminal._UseForTag(pyxb.namespace.ExpandedName(None, 'domain')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 65, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Terminal._UseForTag(pyxb.namespace.ExpandedName(None, 'ipv4addr')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 66, 12))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Terminal._UseForTag(pyxb.namespace.ExpandedName(None, 'virtual_display')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 67, 12))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Terminal._UseForTag(pyxb.namespace.ExpandedName(None, 'location')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 68, 12))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Terminal._Automaton = _BuildAutomaton_2()




Terminals._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'terminal'), Terminal, scope=Terminals, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 117, 12)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Terminals._UseForTag(pyxb.namespace.ExpandedName(None, 'terminal')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 117, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Terminals._Automaton = _BuildAutomaton_3()




Address._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'street'), pyxb.binding.datatypes.string, scope=Address, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 186, 12)))

Address._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'house_number'), pyxb.binding.datatypes.string, scope=Address, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 187, 12)))

Address._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'city'), pyxb.binding.datatypes.string, scope=Address, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 188, 12)))

Address._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'zip_code'), pyxb.binding.datatypes.string, scope=Address, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 189, 12)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Address._UseForTag(pyxb.namespace.ExpandedName(None, 'street')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 186, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Address._UseForTag(pyxb.namespace.ExpandedName(None, 'house_number')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 187, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Address._UseForTag(pyxb.namespace.ExpandedName(None, 'city')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 188, 12))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Address._UseForTag(pyxb.namespace.ExpandedName(None, 'zip_code')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 189, 12))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Address._Automaton = _BuildAutomaton_4()




Message._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'text'), Text, scope=Message, documentation="\n                        The messages' body or content\n                    ", location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 265, 12)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Message._UseForTag(pyxb.namespace.ExpandedName(None, 'text')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 265, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Message._Automaton = _BuildAutomaton_5()




TerminalDetail._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'status'), TerminalStatus, scope=TerminalDetail, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 97, 20)))

TerminalDetail._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'uptime'), pyxb.binding.datatypes.unsignedLong, scope=TerminalDetail, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 98, 20)))

TerminalDetail._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'screenshot'), Screenshot, scope=TerminalDetail, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 99, 20)))

TerminalDetail._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'touch_event'), TouchEvent, scope=TerminalDetail, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 100, 20)))

TerminalDetail._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'setup_operator'), SetupOperator, scope=TerminalDetail, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 101, 20)))

TerminalDetail._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'administrator'), Administrator, scope=TerminalDetail, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 102, 20)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 67, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 99, 20))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 100, 20))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 101, 20))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 102, 20))
    counters.add(cc_4)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(TerminalDetail._UseForTag(pyxb.namespace.ExpandedName(None, 'cls')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 64, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(TerminalDetail._UseForTag(pyxb.namespace.ExpandedName(None, 'domain')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 65, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(TerminalDetail._UseForTag(pyxb.namespace.ExpandedName(None, 'ipv4addr')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 66, 12))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(TerminalDetail._UseForTag(pyxb.namespace.ExpandedName(None, 'virtual_display')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 67, 12))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(TerminalDetail._UseForTag(pyxb.namespace.ExpandedName(None, 'location')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 68, 12))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(TerminalDetail._UseForTag(pyxb.namespace.ExpandedName(None, 'status')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 97, 20))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(TerminalDetail._UseForTag(pyxb.namespace.ExpandedName(None, 'uptime')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 98, 20))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(TerminalDetail._UseForTag(pyxb.namespace.ExpandedName(None, 'screenshot')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 99, 20))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(TerminalDetail._UseForTag(pyxb.namespace.ExpandedName(None, 'touch_event')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 100, 20))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(TerminalDetail._UseForTag(pyxb.namespace.ExpandedName(None, 'setup_operator')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 101, 20))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(TerminalDetail._UseForTag(pyxb.namespace.ExpandedName(None, 'administrator')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/terminallib/doc/terminallib.xsd', 102, 20))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
         ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
         ]))
    transitions.append(fac.Transition(st_8, [
         ]))
    transitions.append(fac.Transition(st_9, [
         ]))
    transitions.append(fac.Transition(st_10, [
         ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, True) ]))
    st_10._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
TerminalDetail._Automaton = _BuildAutomaton_6()

