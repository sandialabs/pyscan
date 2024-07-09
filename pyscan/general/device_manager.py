from item_attribute import ItemAttribute
from pyvisa import ResourceManager, VisaIOError


class DeviceManager(ItemAttribute):
    '''
    Class to hold and control device objects to be used in experiments that includes useful methods.
    '''

    def __init__(self, dictionary=None):
        super().__init__(dictionary)
        self.resource_manager = ResourceManager()
        self.resources_listed = self.resource_manager.list_resources()

    def update_resources_listed(self):
        '''
        Updates the device manager object's resources_listed.
        '''
        self.resources_listed = self.resource_manager.list_resources()

    def list_resource_ids(self):
        """
        Prints a list of resource addresses paired with their ID strings if available.
        """
        self.update_resources_listed()

        for r in self.resources_listed:
            try:
                # Connect to the instrument
                res = self.resource_manager.open_resource(r)
            except VisaIOError as e:
                print(f"{e}\n Could not connect to instrument {r}, may already be connected elsewhere.")
                continue

            try:
                # Try to query the I.D. of the instrument
                name = res.query('*IDN?')
                # If found, print the resource as well as the I.D.
                print(r, name)
            except VisaIOError:
                pass

            # Important. Close the connection.
            res.close()
