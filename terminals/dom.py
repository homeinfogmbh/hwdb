# ./terminals.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:e0f2b2b6088681bd91db874b9eaa9b60ccb9bc46
# Generated 2015-07-31 14:01:57.257010 by PyXB version 1.2.5-DEV using Python 3.4.3.final.0
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
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:f1326e6a-377b-11e5-80ab-7427eaa9df7d')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.5-DEV'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

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


# Atomic simple type: {http://xml.homeinfo.de/schema/terminallib}IPv4Address
class IPv4Address (pyxb.binding.datatypes.string):

    """
                An IPv4 address
            """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'IPv4Address')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 446, 4)
    _Documentation = '\n                An IPv4 address\n            '
IPv4Address._CF_pattern = pyxb.binding.facets.CF_pattern()
IPv4Address._CF_pattern.addPattern(pattern='(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])\\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])\\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])\\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])')
IPv4Address._InitializeFacetMap(IPv4Address._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'IPv4Address', IPv4Address)
_module_typeBindings.IPv4Address = IPv4Address

# Atomic simple type: {http://xml.homeinfo.de/schema/terminallib}UUID4
class UUID4 (pyxb.binding.datatypes.string):

    """A Universally Unique Identifier"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'UUID4')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 461, 4)
    _Documentation = 'A Universally Unique Identifier'
UUID4._CF_pattern = pyxb.binding.facets.CF_pattern()
UUID4._CF_pattern.addPattern(pattern='[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}')
UUID4._InitializeFacetMap(UUID4._CF_pattern)
Namespace.addCategoryObject('typeBinding', 'UUID4', UUID4)
_module_typeBindings.UUID4 = UUID4

# Complex type {http://xml.homeinfo.de/schema/terminallib}Class with content type SIMPLE
class Class (pyxb.binding.basis.complexTypeDefinition):
    """
                Terminal class
            """
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Class')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 130, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpxml_homeinfo_deschematerminallib_Class_id', pyxb.binding.datatypes.integer)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 138, 16)
    __id._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 138, 16)
    
    id = property(__id.value, __id.set, None, "\n                            The appropriate record's ID\n                        ")

    
    # Attribute full_name uses Python identifier full_name
    __full_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'full_name'), 'full_name', '__httpxml_homeinfo_deschematerminallib_Class_full_name', pyxb.binding.datatypes.string)
    __full_name._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 145, 16)
    __full_name._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 145, 16)
    
    full_name = property(__full_name.value, __full_name.set, None, '\n                            A verbose name\n                        ')

    
    # Attribute touch uses Python identifier touch
    __touch = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'touch'), 'touch', '__httpxml_homeinfo_deschematerminallib_Class_touch', pyxb.binding.datatypes.boolean, required=True)
    __touch._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 152, 16)
    __touch._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 152, 16)
    
    touch = property(__touch.value, __touch.set, None, '\n                            Flag whether it is a class with touch screen\n                        ')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __id.name() : __id,
        __full_name.name() : __full_name,
        __touch.name() : __touch
    })
_module_typeBindings.Class = Class
Namespace.addCategoryObject('typeBinding', 'Class', Class)


# Complex type {http://xml.homeinfo.de/schema/terminallib}Domain with content type SIMPLE
class Domain (pyxb.binding.basis.complexTypeDefinition):
    """
                Terminal domain
            """
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Domain')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 165, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpxml_homeinfo_deschematerminallib_Domain_id', pyxb.binding.datatypes.integer)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 173, 16)
    __id._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 173, 16)
    
    id = property(__id.value, __id.set, None, "\n                            The appropriate record's ID\n                        ")

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __id.name() : __id
    })
_module_typeBindings.Domain = Domain
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
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 186, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element street uses Python identifier street
    __street = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'street'), 'street', '__httpxml_homeinfo_deschematerminallib_Address_street', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 193, 12), )

    
    street = property(__street.value, __street.set, None, None)

    
    # Element house_number uses Python identifier house_number
    __house_number = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'house_number'), 'house_number', '__httpxml_homeinfo_deschematerminallib_Address_house_number', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 194, 12), )

    
    house_number = property(__house_number.value, __house_number.set, None, None)

    
    # Element city uses Python identifier city
    __city = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'city'), 'city', '__httpxml_homeinfo_deschematerminallib_Address_city', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 195, 12), )

    
    city = property(__city.value, __city.set, None, None)

    
    # Element zip_code uses Python identifier zip_code
    __zip_code = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'zip_code'), 'zip_code', '__httpxml_homeinfo_deschematerminallib_Address_zip_code', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 196, 12), )

    
    zip_code = property(__zip_code.value, __zip_code.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpxml_homeinfo_deschematerminallib_Address_id', pyxb.binding.datatypes.integer)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 198, 8)
    __id._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 198, 8)
    
    id = property(__id.value, __id.set, None, "\n                    The appropriate record's ID\n                ")

    _ElementMap.update({
        __street.name() : __street,
        __house_number.name() : __house_number,
        __city.name() : __city,
        __zip_code.name() : __zip_code
    })
    _AttributeMap.update({
        __id.name() : __id
    })
_module_typeBindings.Address = Address
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
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 209, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.base64Binary
    
    # Attribute tid uses Python identifier tid
    __tid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'tid'), 'tid', '__httpxml_homeinfo_deschematerminallib_Screenshot_tid', pyxb.binding.datatypes.integer, required=True)
    __tid._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 217, 16)
    __tid._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 217, 16)
    
    tid = property(__tid.value, __tid.set, None, "\n                            The appropriate terminal's ID\n                        ")

    
    # Attribute cid uses Python identifier cid
    __cid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'cid'), 'cid', '__httpxml_homeinfo_deschematerminallib_Screenshot_cid', pyxb.binding.datatypes.integer, required=True)
    __cid._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 224, 16)
    __cid._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 224, 16)
    
    cid = property(__cid.value, __cid.set, None, "\n                            The appropriate terminal's customer's ID\n                        ")

    
    # Attribute timestamp uses Python identifier timestamp
    __timestamp = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'timestamp'), 'timestamp', '__httpxml_homeinfo_deschematerminallib_Screenshot_timestamp', pyxb.binding.datatypes.dateTime, required=True)
    __timestamp._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 231, 16)
    __timestamp._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 231, 16)
    
    timestamp = property(__timestamp.value, __timestamp.set, None, '\n                            The time, when the screenshot was taken\n                        ')

    
    # Attribute mimetype uses Python identifier mimetype
    __mimetype = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'mimetype'), 'mimetype', '__httpxml_homeinfo_deschematerminallib_Screenshot_mimetype', pyxb.binding.datatypes.string, required=True)
    __mimetype._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 238, 16)
    __mimetype._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 238, 16)
    
    mimetype = property(__mimetype.value, __mimetype.set, None, "\n                            The screenshot picture's mime type\n                        ")

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __tid.name() : __tid,
        __cid.name() : __cid,
        __timestamp.name() : __timestamp,
        __mimetype.name() : __mimetype
    })
_module_typeBindings.Screenshot = Screenshot
Namespace.addCategoryObject('typeBinding', 'Screenshot', Screenshot)


# Complex type {http://xml.homeinfo.de/schema/terminallib}Customer with content type SIMPLE
class Customer (pyxb.binding.basis.complexTypeDefinition):
    """
                Localized text string
            """
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Customer')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 251, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute cid uses Python identifier cid
    __cid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'cid'), 'cid', '__httpxml_homeinfo_deschematerminallib_Customer_cid', pyxb.binding.datatypes.integer, required=True)
    __cid._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 259, 16)
    __cid._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 259, 16)
    
    cid = property(__cid.value, __cid.set, None, "\n                            The customer's ID\n                        ")

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __cid.name() : __cid
    })
_module_typeBindings.Customer = Customer
Namespace.addCategoryObject('typeBinding', 'Customer', Customer)


# Complex type {http://xml.homeinfo.de/schema/terminallib}WebConsole with content type ELEMENT_ONLY
class WebConsole (pyxb.binding.basis.complexTypeDefinition):
    """
                Localized text string
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'WebConsole')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 272, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element prompt uses Python identifier prompt
    __prompt = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'prompt'), 'prompt', '__httpxml_homeinfo_deschematerminallib_WebConsole_prompt', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 279, 12), )

    
    prompt = property(__prompt.value, __prompt.set, None, None)

    
    # Element reply uses Python identifier reply
    __reply = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'reply'), 'reply', '__httpxml_homeinfo_deschematerminallib_WebConsole_reply', True, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 280, 12), )

    
    reply = property(__reply.value, __reply.set, None, None)

    _ElementMap.update({
        __prompt.name() : __prompt,
        __reply.name() : __reply
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.WebConsole = WebConsole
Namespace.addCategoryObject('typeBinding', 'WebConsole', WebConsole)


# Complex type {http://xml.homeinfo.de/schema/terminallib}TerminalResult with content type ELEMENT_ONLY
class TerminalResult (pyxb.binding.basis.complexTypeDefinition):
    """
                Localized text string
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TerminalResult')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 286, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element exit_code uses Python identifier exit_code
    __exit_code = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'exit_code'), 'exit_code', '__httpxml_homeinfo_deschematerminallib_TerminalResult_exit_code', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 293, 12), )

    
    exit_code = property(__exit_code.value, __exit_code.set, None, '\n                        The return code\n                    ')

    
    # Element stdout uses Python identifier stdout
    __stdout = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'stdout'), 'stdout', '__httpxml_homeinfo_deschematerminallib_TerminalResult_stdout', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 300, 12), )

    
    stdout = property(__stdout.value, __stdout.set, None, '\n                        Text of the STDOUT\n                    ')

    
    # Element stderr uses Python identifier stderr
    __stderr = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'stderr'), 'stderr', '__httpxml_homeinfo_deschematerminallib_TerminalResult_stderr', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 307, 12), )

    
    stderr = property(__stderr.value, __stderr.set, None, '\n                        Text of the STDERR\n                    ')

    
    # Attribute timestamp uses Python identifier timestamp
    __timestamp = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'timestamp'), 'timestamp', '__httpxml_homeinfo_deschematerminallib_TerminalResult_timestamp', pyxb.binding.datatypes.dateTime, required=True)
    __timestamp._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 315, 8)
    __timestamp._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 315, 8)
    
    timestamp = property(__timestamp.value, __timestamp.set, None, '\n                    A time stamp\n                ')

    
    # Attribute cid uses Python identifier cid
    __cid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'cid'), 'cid', '__httpxml_homeinfo_deschematerminallib_TerminalResult_cid', pyxb.binding.datatypes.integer, required=True)
    __cid._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 322, 8)
    __cid._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 322, 8)
    
    cid = property(__cid.value, __cid.set, None, '\n                    The customer ID\n                ')

    
    # Attribute tid uses Python identifier tid
    __tid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'tid'), 'tid', '__httpxml_homeinfo_deschematerminallib_TerminalResult_tid', pyxb.binding.datatypes.integer, required=True)
    __tid._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 329, 8)
    __tid._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 329, 8)
    
    tid = property(__tid.value, __tid.set, None, '\n                    The terminal ID\n                ')

    _ElementMap.update({
        __exit_code.name() : __exit_code,
        __stdout.name() : __stdout,
        __stderr.name() : __stderr
    })
    _AttributeMap.update({
        __timestamp.name() : __timestamp,
        __cid.name() : __cid,
        __tid.name() : __tid
    })
_module_typeBindings.TerminalResult = TerminalResult
Namespace.addCategoryObject('typeBinding', 'TerminalResult', TerminalResult)


# Complex type {http://xml.homeinfo.de/schema/terminallib}Message with content type ELEMENT_ONLY
class Message (pyxb.binding.basis.complexTypeDefinition):
    """
                Messages
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Message')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 340, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element text uses Python identifier text
    __text = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'text'), 'text', '__httpxml_homeinfo_deschematerminallib_Message_text', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 347, 12), )

    
    text = property(__text.value, __text.set, None, "\n                        The messages' body or content\n                    ")

    
    # Attribute code uses Python identifier code
    __code = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'code'), 'code', '__httpxml_homeinfo_deschematerminallib_Message_code', pyxb.binding.datatypes.integer, required=True)
    __code._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 355, 8)
    __code._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 355, 8)
    
    code = property(__code.value, __code.set, None, '\n                    A unique message code\n                ')

    _ElementMap.update({
        __text.name() : __text
    })
    _AttributeMap.update({
        __code.name() : __code
    })
_module_typeBindings.Message = Message
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
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 366, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute lang uses Python identifier lang
    __lang = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'lang'), 'lang', '__httpxml_homeinfo_deschematerminallib_Text_lang', pyxb.binding.datatypes.string, required=True)
    __lang._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 374, 16)
    __lang._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 374, 16)
    
    lang = property(__lang.value, __lang.set, None, '\n                            The language of the text\n                        ')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __lang.name() : __lang
    })
_module_typeBindings.Text = Text
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
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 387, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpxml_homeinfo_deschematerminallib_SetupOperator_id', pyxb.binding.datatypes.integer, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 395, 16)
    __id._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 395, 16)
    
    id = property(__id.value, __id.set, None, '\n                            The ID of the operator\n                        ')

    
    # Attribute annotation uses Python identifier annotation
    __annotation = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'annotation'), 'annotation', '__httpxml_homeinfo_deschematerminallib_SetupOperator_annotation', pyxb.binding.datatypes.string)
    __annotation._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 402, 16)
    __annotation._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 402, 16)
    
    annotation = property(__annotation.value, __annotation.set, None, '\n                            An optional annotation\n                        ')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __id.name() : __id,
        __annotation.name() : __annotation
    })
_module_typeBindings.SetupOperator = SetupOperator
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
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 415, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpxml_homeinfo_deschematerminallib_Administrator_id', pyxb.binding.datatypes.integer, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 423, 16)
    __id._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 423, 16)
    
    id = property(__id.value, __id.set, None, '\n                            The ID of the administrator\n                        ')

    
    # Attribute annotation uses Python identifier annotation
    __annotation = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'annotation'), 'annotation', '__httpxml_homeinfo_deschematerminallib_Administrator_annotation', pyxb.binding.datatypes.string)
    __annotation._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 430, 16)
    __annotation._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 430, 16)
    
    annotation = property(__annotation.value, __annotation.set, None, '\n                            An optional annotation\n                        ')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __id.name() : __id,
        __annotation.name() : __annotation
    })
_module_typeBindings.Administrator = Administrator
Namespace.addCategoryObject('typeBinding', 'Administrator', Administrator)


# Complex type {http://xml.homeinfo.de/schema/terminallib}TerminalLibrary with content type ELEMENT_ONLY
class TerminalLibrary (pyxb.binding.basis.complexTypeDefinition):
    """
                A terminal web API solution by HOMEINFO Digitale Informationssysteme GmbH
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TerminalLibrary')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 12, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element terminal uses Python identifier terminal
    __terminal = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'terminal'), 'terminal', '__httpxml_homeinfo_deschematerminallib_TerminalLibrary_terminal', True, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 20, 16), )

    
    terminal = property(__terminal.value, __terminal.set, None, None)

    
    # Element details uses Python identifier details
    __details = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'details'), 'details', '__httpxml_homeinfo_deschematerminallib_TerminalLibrary_details', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 21, 16), )

    
    details = property(__details.value, __details.set, None, None)

    
    # Element console uses Python identifier console
    __console = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'console'), 'console', '__httpxml_homeinfo_deschematerminallib_TerminalLibrary_console', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 22, 16), )

    
    console = property(__console.value, __console.set, None, None)

    
    # Element screenshot uses Python identifier screenshot
    __screenshot = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'screenshot'), 'screenshot', '__httpxml_homeinfo_deschematerminallib_TerminalLibrary_screenshot', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 23, 16), )

    
    screenshot = property(__screenshot.value, __screenshot.set, None, None)

    
    # Element class uses Python identifier class_
    __class = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'class'), 'class_', '__httpxml_homeinfo_deschematerminallib_TerminalLibrary_class', True, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 24, 16), )

    
    class_ = property(__class.value, __class.set, None, None)

    
    # Element domain uses Python identifier domain
    __domain = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'domain'), 'domain', '__httpxml_homeinfo_deschematerminallib_TerminalLibrary_domain', True, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 25, 16), )

    
    domain = property(__domain.value, __domain.set, None, None)

    
    # Element setup_operator uses Python identifier setup_operator
    __setup_operator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'setup_operator'), 'setup_operator', '__httpxml_homeinfo_deschematerminallib_TerminalLibrary_setup_operator', True, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 26, 16), )

    
    setup_operator = property(__setup_operator.value, __setup_operator.set, None, None)

    
    # Element administrator uses Python identifier administrator
    __administrator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'administrator'), 'administrator', '__httpxml_homeinfo_deschematerminallib_TerminalLibrary_administrator', True, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 27, 16), )

    
    administrator = property(__administrator.value, __administrator.set, None, None)

    
    # Attribute session_token uses Python identifier session_token
    __session_token = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'session_token'), 'session_token', '__httpxml_homeinfo_deschematerminallib_TerminalLibrary_session_token', _module_typeBindings.UUID4)
    __session_token._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 30, 8)
    __session_token._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 30, 8)
    
    session_token = property(__session_token.value, __session_token.set, None, '\n                    A session token\n                ')

    _ElementMap.update({
        __terminal.name() : __terminal,
        __details.name() : __details,
        __console.name() : __console,
        __screenshot.name() : __screenshot,
        __class.name() : __class,
        __domain.name() : __domain,
        __setup_operator.name() : __setup_operator,
        __administrator.name() : __administrator
    })
    _AttributeMap.update({
        __session_token.name() : __session_token
    })
_module_typeBindings.TerminalLibrary = TerminalLibrary
Namespace.addCategoryObject('typeBinding', 'TerminalLibrary', TerminalLibrary)


# Complex type {http://xml.homeinfo.de/schema/terminallib}BasicTerminalInfo with content type ELEMENT_ONLY
class BasicTerminalInfo (pyxb.binding.basis.complexTypeDefinition):
    """
                Basic terminal information
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'BasicTerminalInfo')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 41, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element class uses Python identifier class_
    __class = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'class'), 'class_', '__httpxml_homeinfo_deschematerminallib_BasicTerminalInfo_class', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 48, 12), )

    
    class_ = property(__class.value, __class.set, None, "\n                        The terminal's class\n                    ")

    
    # Element domain uses Python identifier domain
    __domain = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'domain'), 'domain', '__httpxml_homeinfo_deschematerminallib_BasicTerminalInfo_domain', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 55, 12), )

    
    domain = property(__domain.value, __domain.set, None, "\n                        The terminal's domain\n                    ")

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpxml_homeinfo_deschematerminallib_BasicTerminalInfo_id', pyxb.binding.datatypes.integer)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 63, 8)
    __id._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 63, 8)
    
    id = property(__id.value, __id.set, None, "\n                    The appropriate record's ID\n                ")

    
    # Attribute tid uses Python identifier tid
    __tid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'tid'), 'tid', '__httpxml_homeinfo_deschematerminallib_BasicTerminalInfo_tid', pyxb.binding.datatypes.integer, required=True)
    __tid._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 70, 8)
    __tid._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 70, 8)
    
    tid = property(__tid.value, __tid.set, None, '\n                    The terminal identifier\n                ')

    
    # Attribute cid uses Python identifier cid
    __cid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'cid'), 'cid', '__httpxml_homeinfo_deschematerminallib_BasicTerminalInfo_cid', pyxb.binding.datatypes.integer, required=True)
    __cid._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 77, 8)
    __cid._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 77, 8)
    
    cid = property(__cid.value, __cid.set, None, '\n                    The customer identifier\n                ')

    
    # Attribute deleted uses Python identifier deleted
    __deleted = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'deleted'), 'deleted', '__httpxml_homeinfo_deschematerminallib_BasicTerminalInfo_deleted', pyxb.binding.datatypes.dateTime)
    __deleted._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 84, 8)
    __deleted._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 84, 8)
    
    deleted = property(__deleted.value, __deleted.set, None, '\n                    Date and time when the terminal was deleted. If missing, terminal is not deleted.\n                ')

    
    # Attribute status uses Python identifier status
    __status = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'status'), 'status', '__httpxml_homeinfo_deschematerminallib_BasicTerminalInfo_status', pyxb.binding.datatypes.boolean, required=True)
    __status._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 91, 8)
    __status._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 91, 8)
    
    status = property(__status.value, __status.set, None, "\n                    The terminal's current status\n                ")

    
    # Attribute ipv4addr uses Python identifier ipv4addr
    __ipv4addr = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ipv4addr'), 'ipv4addr', '__httpxml_homeinfo_deschematerminallib_BasicTerminalInfo_ipv4addr', _module_typeBindings.IPv4Address, required=True)
    __ipv4addr._DeclarationLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 98, 8)
    __ipv4addr._UseLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 98, 8)
    
    ipv4addr = property(__ipv4addr.value, __ipv4addr.set, None, "\n                    The terminal's IPv4 address identifier\n                ")

    _ElementMap.update({
        __class.name() : __class,
        __domain.name() : __domain
    })
    _AttributeMap.update({
        __id.name() : __id,
        __tid.name() : __tid,
        __cid.name() : __cid,
        __deleted.name() : __deleted,
        __status.name() : __status,
        __ipv4addr.name() : __ipv4addr
    })
_module_typeBindings.BasicTerminalInfo = BasicTerminalInfo
Namespace.addCategoryObject('typeBinding', 'BasicTerminalInfo', BasicTerminalInfo)


# Complex type {http://xml.homeinfo.de/schema/terminallib}TerminalDetails with content type ELEMENT_ONLY
class TerminalDetails (BasicTerminalInfo):
    """
                More detailed terminal information
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'TerminalDetails')
    _XSDLocation = pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 109, 4)
    _ElementMap = BasicTerminalInfo._ElementMap.copy()
    _AttributeMap = BasicTerminalInfo._AttributeMap.copy()
    # Base type is BasicTerminalInfo
    
    # Element class_ (class) inherited from {http://xml.homeinfo.de/schema/terminallib}BasicTerminalInfo
    
    # Element domain (domain) inherited from {http://xml.homeinfo.de/schema/terminallib}BasicTerminalInfo
    
    # Element customer uses Python identifier customer
    __customer = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'customer'), 'customer', '__httpxml_homeinfo_deschematerminallib_TerminalDetails_customer', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 118, 20), )

    
    customer = property(__customer.value, __customer.set, None, None)

    
    # Element location uses Python identifier location
    __location = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'location'), 'location', '__httpxml_homeinfo_deschematerminallib_TerminalDetails_location', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 119, 20), )

    
    location = property(__location.value, __location.set, None, None)

    
    # Element uptime uses Python identifier uptime
    __uptime = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'uptime'), 'uptime', '__httpxml_homeinfo_deschematerminallib_TerminalDetails_uptime', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 120, 20), )

    
    uptime = property(__uptime.value, __uptime.set, None, None)

    
    # Element virtual_display uses Python identifier virtual_display
    __virtual_display = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'virtual_display'), 'virtual_display', '__httpxml_homeinfo_deschematerminallib_TerminalDetails_virtual_display', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 121, 20), )

    
    virtual_display = property(__virtual_display.value, __virtual_display.set, None, None)

    
    # Element screenshot uses Python identifier screenshot
    __screenshot = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'screenshot'), 'screenshot', '__httpxml_homeinfo_deschematerminallib_TerminalDetails_screenshot', False, pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 122, 20), )

    
    screenshot = property(__screenshot.value, __screenshot.set, None, None)

    
    # Attribute id inherited from {http://xml.homeinfo.de/schema/terminallib}BasicTerminalInfo
    
    # Attribute tid inherited from {http://xml.homeinfo.de/schema/terminallib}BasicTerminalInfo
    
    # Attribute cid inherited from {http://xml.homeinfo.de/schema/terminallib}BasicTerminalInfo
    
    # Attribute deleted inherited from {http://xml.homeinfo.de/schema/terminallib}BasicTerminalInfo
    
    # Attribute status inherited from {http://xml.homeinfo.de/schema/terminallib}BasicTerminalInfo
    
    # Attribute ipv4addr inherited from {http://xml.homeinfo.de/schema/terminallib}BasicTerminalInfo
    _ElementMap.update({
        __customer.name() : __customer,
        __location.name() : __location,
        __uptime.name() : __uptime,
        __virtual_display.name() : __virtual_display,
        __screenshot.name() : __screenshot
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.TerminalDetails = TerminalDetails
Namespace.addCategoryObject('typeBinding', 'TerminalDetails', TerminalDetails)


terminals = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'terminals'), TerminalLibrary, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 8, 4))
Namespace.addCategoryObject('elementBinding', terminals.name().localName(), terminals)



Address._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'street'), pyxb.binding.datatypes.string, scope=Address, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 193, 12)))

Address._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'house_number'), pyxb.binding.datatypes.string, scope=Address, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 194, 12)))

Address._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'city'), pyxb.binding.datatypes.string, scope=Address, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 195, 12)))

Address._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'zip_code'), pyxb.binding.datatypes.string, scope=Address, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 196, 12)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Address._UseForTag(pyxb.namespace.ExpandedName(None, 'street')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 193, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Address._UseForTag(pyxb.namespace.ExpandedName(None, 'house_number')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 194, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Address._UseForTag(pyxb.namespace.ExpandedName(None, 'city')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 195, 12))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Address._UseForTag(pyxb.namespace.ExpandedName(None, 'zip_code')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 196, 12))
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
Address._Automaton = _BuildAutomaton()




WebConsole._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'prompt'), pyxb.binding.datatypes.string, scope=WebConsole, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 279, 12)))

WebConsole._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'reply'), TerminalResult, scope=WebConsole, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 280, 12)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 280, 12))
    counters.add(cc_0)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(WebConsole._UseForTag(pyxb.namespace.ExpandedName(None, 'prompt')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 279, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(WebConsole._UseForTag(pyxb.namespace.ExpandedName(None, 'reply')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 280, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
WebConsole._Automaton = _BuildAutomaton_()




TerminalResult._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'exit_code'), pyxb.binding.datatypes.byte, scope=TerminalResult, documentation='\n                        The return code\n                    ', location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 293, 12)))

TerminalResult._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'stdout'), pyxb.binding.datatypes.string, scope=TerminalResult, documentation='\n                        Text of the STDOUT\n                    ', location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 300, 12)))

TerminalResult._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'stderr'), pyxb.binding.datatypes.string, scope=TerminalResult, documentation='\n                        Text of the STDERR\n                    ', location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 307, 12)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 300, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 307, 12))
    counters.add(cc_1)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(TerminalResult._UseForTag(pyxb.namespace.ExpandedName(None, 'exit_code')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 293, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(TerminalResult._UseForTag(pyxb.namespace.ExpandedName(None, 'stdout')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 300, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(TerminalResult._UseForTag(pyxb.namespace.ExpandedName(None, 'stderr')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 307, 12))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
TerminalResult._Automaton = _BuildAutomaton_2()




Message._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'text'), Text, scope=Message, documentation="\n                        The messages' body or content\n                    ", location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 347, 12)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Message._UseForTag(pyxb.namespace.ExpandedName(None, 'text')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 347, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Message._Automaton = _BuildAutomaton_3()




TerminalLibrary._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'terminal'), BasicTerminalInfo, scope=TerminalLibrary, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 20, 16)))

TerminalLibrary._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'details'), TerminalDetails, scope=TerminalLibrary, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 21, 16)))

TerminalLibrary._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'console'), WebConsole, scope=TerminalLibrary, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 22, 16)))

TerminalLibrary._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'screenshot'), Screenshot, scope=TerminalLibrary, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 23, 16)))

TerminalLibrary._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'class'), Class, scope=TerminalLibrary, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 24, 16)))

TerminalLibrary._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'domain'), Domain, scope=TerminalLibrary, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 25, 16)))

TerminalLibrary._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'setup_operator'), SetupOperator, scope=TerminalLibrary, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 26, 16)))

TerminalLibrary._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'administrator'), Administrator, scope=TerminalLibrary, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 27, 16)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 24, 16))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 25, 16))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 26, 16))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 27, 16))
    counters.add(cc_3)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(TerminalLibrary._UseForTag(pyxb.namespace.ExpandedName(None, 'terminal')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 20, 16))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(TerminalLibrary._UseForTag(pyxb.namespace.ExpandedName(None, 'details')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 21, 16))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(TerminalLibrary._UseForTag(pyxb.namespace.ExpandedName(None, 'console')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 22, 16))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(TerminalLibrary._UseForTag(pyxb.namespace.ExpandedName(None, 'screenshot')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 23, 16))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(TerminalLibrary._UseForTag(pyxb.namespace.ExpandedName(None, 'class')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 24, 16))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(TerminalLibrary._UseForTag(pyxb.namespace.ExpandedName(None, 'domain')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 25, 16))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(TerminalLibrary._UseForTag(pyxb.namespace.ExpandedName(None, 'setup_operator')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 26, 16))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(TerminalLibrary._UseForTag(pyxb.namespace.ExpandedName(None, 'administrator')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 27, 16))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    transitions = []
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_7._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
TerminalLibrary._Automaton = _BuildAutomaton_4()




BasicTerminalInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'class'), Class, scope=BasicTerminalInfo, documentation="\n                        The terminal's class\n                    ", location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 48, 12)))

BasicTerminalInfo._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'domain'), Domain, scope=BasicTerminalInfo, documentation="\n                        The terminal's domain\n                    ", location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 55, 12)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(BasicTerminalInfo._UseForTag(pyxb.namespace.ExpandedName(None, 'class')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 48, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(BasicTerminalInfo._UseForTag(pyxb.namespace.ExpandedName(None, 'domain')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 55, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
BasicTerminalInfo._Automaton = _BuildAutomaton_5()




TerminalDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'customer'), Customer, scope=TerminalDetails, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 118, 20)))

TerminalDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'location'), Address, scope=TerminalDetails, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 119, 20)))

TerminalDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'uptime'), pyxb.binding.datatypes.unsignedLong, scope=TerminalDetails, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 120, 20)))

TerminalDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'virtual_display'), pyxb.binding.datatypes.integer, scope=TerminalDetails, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 121, 20)))

TerminalDetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'screenshot'), pyxb.binding.datatypes.base64Binary, scope=TerminalDetails, location=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 122, 20)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 121, 20))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 122, 20))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(TerminalDetails._UseForTag(pyxb.namespace.ExpandedName(None, 'class')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 48, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(TerminalDetails._UseForTag(pyxb.namespace.ExpandedName(None, 'domain')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 55, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(TerminalDetails._UseForTag(pyxb.namespace.ExpandedName(None, 'customer')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 118, 20))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(TerminalDetails._UseForTag(pyxb.namespace.ExpandedName(None, 'location')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 119, 20))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(TerminalDetails._UseForTag(pyxb.namespace.ExpandedName(None, 'uptime')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 120, 20))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(TerminalDetails._UseForTag(pyxb.namespace.ExpandedName(None, 'virtual_display')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 121, 20))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(TerminalDetails._UseForTag(pyxb.namespace.ExpandedName(None, 'screenshot')), pyxb.utils.utility.Location('/home/rne/Dokumente/Programmierung/python/homeinfo-terminals/doc/terminals.xsd', 122, 20))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
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
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
TerminalDetails._Automaton = _BuildAutomaton_6()

