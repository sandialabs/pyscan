import re
from ...general.item_attribute import ItemAttribute


class AbstractDriver(ItemAttribute):
    '''
    None
    '''
    def __init__(self, instrument=None, debug=False):
        self.instrument = instrument
        self.debug = debug

    @property
    def name(self):
        return [k for k, v in globals().items() if v is self]

    def initialize_properties(self):
        pass

    def write(self):
        pass

    def query(self):
        pass

    def read(self):
        pass

    def add_device_property(self, settings):

        name = settings['name']
        # Make self._name_settings
        settings_name = '_' + name + '_settings'
        property_settings = self.property_class(self, settings)
        setattr(self, settings_name, property_settings)

        # Make self.name property
        property_definition = property(
            fget=getattr(self, settings_name).get_property,
            fset=lambda obj, new_value: getattr(self, settings_name).set_property(obj, new_value),
            doc=self.get_property_docstring(name))
        setattr(self.__class__, name, property_definition)

    @property
    def version(self):
        return self._version

    def update_properties(self):
        properties = self.get_pyscan_properties()

        for prop in properties:
            settings = self['_{}_settings'.format(prop)]
            if 'write_only' not in settings:
                self[prop]

    def get_pyscan_properties(self):
        '''
        Finds the pyscan style properties of this driver, i.e. those that end with "_settings"

        Returns
        -------
        list :
            list of property names for the current driver
        '''

        r = re.compile(".*_settings")
        pyscan_properties = list(filter(r.match, self.keys()))
        pyscan_properties = [prop[1:] for prop in pyscan_properties]
        pyscan_properties = [prop.replace('_settings', '') for prop in pyscan_properties]
        return pyscan_properties

    def get_property_docstring(self, prop_name):
        '''
        Gets the doc string for a property from an instance of this class

        Parameters
        ----------
        prop_name : str
            The name of the property to get the doc string of

        Returns
        -------
        str :
            The two doc string lines for the property
        '''

        doc = self.__doc__.split('\n')

        r = re.compile("    {} :".format(prop_name))
        match = list(filter(r.match, doc))

        assert len(match) > 0, "No matches for {} documentation".format(prop_name)
        assert len(match) == 1, "Too many matches for {} documentation".format(prop_name)
        match = match[0]

        for i, string in enumerate(doc):
            if string == match:
                break

        doc_string = doc[i][4::]

        for j in range(len(doc_string)):
            try:
                doc[i + 1 + j]
            except:
                break
            if (doc[i + 1 + j][0:1] == '\n') or (len(doc[i + 1 + j][0:7].strip()) != 0):
                # print(repr(doc[i + 1 + j]))
                break
            else:
                doc_string = doc_string + '\n' + doc[i + 1 + j][4::]

        return doc_string
