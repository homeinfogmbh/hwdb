"""Renderable template"""

__date__ = '12.12.2014'
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__all__ = ['Template']


class Template():
    """Template text file that can be rendered"""

    def __init__(self, file_name):
        """Sets the respective text file's path"""
        self._file_name = file_name

    @property
    def text(self):
        """Returns the file's text content"""
        with open(self._file_name, 'r') as txt:
            return txt.read()

    @property
    def data(self):
        """Returns the file's binary content"""
        with open(self._file_name, 'rb') as data:
            return data.read()

    def render(self, rd, dst=None, binary=False):
        """Render the template with the provided dictionary
        and optionally store into the provided <dst> file"""
        if binary:
            temp = self.data
        else:
            temp = self.text
        for k in rd:
            v = rd[k]
            temp = temp.replace(k, v)
        if dst is not None:
            with open(dst, 'wb' if binary else 'w') as dst:
                dst.write(temp)
        return temp
