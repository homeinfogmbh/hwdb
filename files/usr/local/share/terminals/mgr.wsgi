#! /usr/bin/env python3
"""Terminal controller interface

XXX: Please note:

    * This web service must be run as a special user,
      allowed to create and read OpenVPN certs.
      (Do NOT run this as root!)

    * This web service must be HTTPS-Password
      protected by the web server, since it does
      not provide authentication by itself
"""

from termgr.controllers.mgr import TerminalManager

__date__ = "25.03.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"

def application(environ, start_response):
    """Main WSGI method"""
    ctrl = TerminalManager(environ.get('PATH_INFO', ''),
                           environ.get('QUERY_STRING', ''))
    status, response_headers, response_body = ctrl.run()
    start_response(status, response_headers)
    return [response_body]

