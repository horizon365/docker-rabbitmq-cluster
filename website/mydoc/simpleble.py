import time


class SimpleBleClient(object):
    """This is a class implementation of a simple BLE client.
    :param iface: The Bluetooth interface on which to make the connection. On Linux, 0 means `/dev/hci0`, 1 means `/dev/hci1` and so on., defaults to 0
    :type iface: int, optional
    :param scanCallback: A function handle of the form ``callback(client, device, isNewDevice, isNewData)``, where ``client`` is a handle to the :class:`simpleble.SimpleBleClient` that invoked the callback and ``device`` is the detected :class:`simpleble.SimpleBleDevice` object. ``isNewDev`` is `True` if the device (as identified by its MAC address) has not been seen before by the scanner, and `False` otherwise. ``isNewData`` is `True` if new or updated advertising data is available, defaults to None
    :type scanCallback: function, optional
    :param notificationCallback: A function handle of the form ``callback(client, characteristic, data)``, where ``client`` is a handle to the :class:`simpleble.SimpleBleClient` that invoked the callback, ``characteristic`` is the notified :class:`bluepy.blte.Characteristic` object and data is a `bytearray` containing the updated value. Defaults to None
    :type notificationCallback: function, optional
    """

    def __init__(self, iface=0, scanCallback=None, notificationCallback=None):
        """Constructor method
        """

        self._scanner = Scanner(iface) if(scanCallback is None)\
            else Scanner().withDelegate(SimpleBleScanDelegate(scanCallback, self))
        self._iface = iface
        self._discoveredDevices = []
        self._characteristics = []
        self._connected = False
        self._connectedDevice = None
        self._notificationCallback = None

    def setScanCallback(self, callback):
        """Set the callback function to be executed when a device is detected by the client.
        :param callback: A function handle of the form ``callback(client, device, isNewDevice, isNewData)``, where ``client`` is a handle to the :class:`simpleble.SimpleBleClient` that invoked the callback and ``device`` is the detected :class:`simpleble.SimpleBleDevice` object. ``isNewDev`` is `True` if the device (as identified by its MAC address) has not been seen before by the scanner, and `False` otherwise. ``isNewData`` is `True` if new or updated advertising data is available.
        :type callback: function
        """

        self._scanner.withDelegate(
            SimpleBleScanDelegate(callback, client=self))

    def setNotificationCallback(self, callback):
        """Set the callback function to be executed when a device sends a notification to the client.
        :param callback: A function handle of the form ``callback(client, characteristic, data)``, where ``client`` is a handle to the :class:`simpleble.SimpleBleClient` that invoked the callback, ``characteristic`` is the notified :class:`bluepy.blte.Characteristic` object and data is a `bytearray` containing the updated value. Defaults to None
        :type callback: function, optional
        """
        if(self._connectedDevice is not None):
            self._connectedDevice.setNotificationCallback(callback)
        self._notificationCallback = callback

    def scan(self, timeout=10.0):
        """Scans for and returns detected nearby devices
        :param timeout: Specify how long (in seconds) the scan should last, defaults to 10.0
        :type timeout: float, optional
        :return: List of :class:`simpleble.SimpleBleDevice` objects
        :rtype: list
        """

        self._discoveredDevices = []
        scanEntries = self._scanner.scan(timeout)
        for scanEntry in scanEntries:
            self._discoveredDevices.append(
                SimpleBleDevice(
                    client=self,
                    addr=scanEntry.addr,
                    iface=scanEntry.iface,
                    data=scanEntry.getScanData(),
                    rssi=scanEntry.rssi,
                    connectable=scanEntry.connectable, updateCount=scanEntry.updateCount
                )
            )
        return self._discoveredDevices

    def connect(self, device):
        """Attempts to connect client to a given :class:`simpleble.SimpleBleDevice` object and returns a bool indication of the result.
        :param device: An instance of the device to which we want to connect. Normally acquired by calling :meth:`simpleble.SimpleBleClient.scan` or :meth:`simpleble.SimpleBleClient.searchDevice`
        :type device: SimpleBleDevice
        :return: `True` if connection was successful, `False` otherwise
        :rtype: bool
        """
        self._connected = device.connect()
        if(self._connected):
            self._connectedDevice = device
            if(self._notificationCallback is not None):
                self._connectedDevice.setNotificationCallback(
                    self._notificationCallback)
        return self._connected

    def disconnect(self):
        """Drops existing connection.
        Note that the current version of the project assumes that the client can be connected to at most one device at a time.
        """
        self._connectedDevice.disconnect()
        try:
            self._scanner.stop()
        except:
            pass
        self._connectedDevice = None
        self._connected = False

    def isConnected(self):
        """Check to see if client is connected to a device
        :return: `True` if connected, `False` otherwise
        :rtype: bool
        """
        return self._connected

    def getCharacteristics(self, startHnd=1, endHnd=0xFFFF, uuids=None):
        """Returns a list containing :class:`bluepy.btle.Characteristic` objects for the peripheral. If no arguments are given, will return all characteristics. If startHnd and/or endHnd are given, the list is restricted to characteristics whose handles are within the given range.
        :param startHnd: Start index, defaults to 1
        :type startHnd: int, optional
        :param endHnd: End index, defaults to 0xFFFF
        :type endHnd: int, optional
        :param uuids: a list of UUID strings, defaults to None
        :type uuids: list, optional
        :return: List of returned :class:`bluepy.btle.Characteristic` objects
        :rtype: list
        """
        self._characteristics = self._connectedDevice.getCharacteristics(
            startHnd, endHnd, uuids
        )
        return self._characteristics

    def readCharacteristic(self, characteristic=None, uuid=None):
        """Reads the current value of the characteristic identified by either a :class:`bluepy.btle.Characteristic` object ``characteristic``, or a UUID string ``uuid``. If both are provided, then the characteristic will be read on the basis of the ``characteristic`` object. A :class:`bluepy.btle.BTLEException.GATT_ERROR` is raised if no inputs are specified or the requested characteristic was not found.
        :param characteristic: A :class:`bluepy.btle.Characteristic` object, defaults to None
        :type characteristic: :class:`bluepy.btle.Characteristic`, optional
        :param uuid: A given UUID string, defaults to None
        :type uuid: string, optional
        :raises: :class:`bluepy.btle.BTLEException.GATT_ERROR`: If no inputs are specified or the requested characteristic was not found.
        :return: The value read from the characteristic
        :rtype: bytearray
        """
        if(characteristic is None and uuid is not None):
            characteristic = self._connectedDevice.getCharacteristic(
                uuids=[uuid])[0]
        if(characteristic is None):
            raise BTLEException(
                BTLEException.GATT_ERROR, "Characteristic was either not found, given the UUID, or not specified")
        return self._connectedDevice.readCharacteristic(
            characteristic.getHandle())

    def writeCharacteristic(self, val, characteristic=None,
                            uuid=None, withResponse=False):
        """Writes the data val (of type str on Python 2.x, byte on 3.x) to the characteristic identified by either a :class:`bluepy.btle.Characteristic` object ``characteristic``, or a UUID string ``uuid``. If both are provided, then the characteristic will be read on the basis of the ``characteristic`` object. A :class:`bluepy.btle.BTLEException.GATT_ERROR` is raised if no inputs are specified or the requested characteristic was not found. If ``withResponse`` is `True`, the client will await confirmation that the write was successful from the device.
        :param val: Value to be written in characteristic
        :type val: str on Python 2.x, byte on 3.x
        :param characteristic: A :class:`bluepy.btle.Characteristic` object, defaults to None
        :type characteristic: :class:`bluepy.btle.Characteristic`, optional
        :param uuid: A given UUID string, defaults to None
        :type uuid: string, optional
        :param withResponse: If ``withResponse`` is `True`, the client will await confirmation that the write was successful from the device, defaults to False
        :type withResponse: bool, optional
        :raises: :class:`bluepy.btle.BTLEException.GATT_ERROR`: If no inputs are specified or the requested characteristic was not found.
        :return: `True` or `False` indicating success or failure of write operation, in the case that ``withResponce`` is `True`
        :rtype: bool
        """
        if(characteristic is None and uuid is not None):
            characteristic = device.getCharacteristic(uuids=[uuid])
        if(characteristic is None):
            raise BTLEException(
                BTLEException.GATT_ERROR, "Characteristic was either not found, given the UUID, or not specified")
        return self._connectedDevice.writeCharacteristic(characteristic.getHandle(), val, withResponse)

    def searchDevice(self, name=None, mac=None, timeout=10.0):
        """Searches for and returns, given it exists, a :class:`simpleble.SimpleBleDevice` device objects, based on the provided ``name`` and/or ``mac`` address. If both a ``name`` and a ``mac`` are provided, then the client will only return a device that matches both conditions.
        :par    am name: The "Complete Local Name" Generic Access Attribute (GATT) of the device, defaults to None
        :type name: str, optional
        :param mac: The MAC address of the device, defaults to None
        :type mac: str, optional
        :param timeout: Specify how long (in seconds) the scan should last, defaults to 10.0. Internally, it serves as an input to the invoked :meth:`simpleble.SimpleBleClient.scan` method.
        :type timeout: float, optional
        :raises AssertionError: If neither a ``name`` nor a ``mac`` inputs have been provided
        :return: A :class:`simpleble.SimpleBleDevice` object if search was succesfull, None otherwise
        :rtype: :class:`simpleble.SimpleBleDevice` | None
        """
        try:
            check = not (name is None)
            chekc = not (mac is None)
            assert check or chekc
        except AssertionError as e:
            print("Either a name or a mac address must be provided to find a device!")
            raise e
        mode = 0
        if(name is not None):
            mode += 1
        if(mac is not None):
            mode += 1
        # Perform initial detection attempt
        self.scan(timeout)
        for device in self._discoveredDevices:
            found = 0
            if (device.addr == mac):
                found += 1
            for (adtype, desc, value) in device.data:
                if (adtype == 9 and value == name):
                    found += 1
            if(found >= mode):
                return device
        return None

    def printFoundDevices(self):
        """Print all devices discovered during the last scan. Should only be called after a :meth:`simpleble.SimpleBleClient.scan` has been called first.
        """
        for device in self._discoveredDevices:
            print("Device %s (%s), RSSI=%d dB" %
                  (device.addr, device.addrType, device.rssi))
            for (adtype, desc, value) in device.data:
                print("  %s = %s" % (desc, value))





if __name__ == "__main__":
    """This example demonstrates a simple BLE client that scans for devices,
    connects to a device (GATT server) of choice and continuously reads a 
    characteristic on that device.
    """

    # The UUID of the characteristic we want to read and the name of the device # we want to read it from
    Characteristic_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
    Device_Name = "MyESP32"

    # Define our scan and notification callback methods
    def myScanCallback(client, device, isNewDevice, isNewData):
        client._yes = True
        print("#MAC: " + device.addr + " #isNewDevice: " +
              str(isNewDevice) + " #isNewData: " + str(isNewData))
    # TODO: NOTIFICATIONS ARE NOT SUPPORTED YET
    # def myNotificationCallback(client, characteristic, data):
    #     print("Notification received!")
    #     print("  Characteristic UUID: " + characteristic.uuid)
    #     print("  Data: " + str(data))

    # Instantiate a SimpleBleClient and set it's scan callback
    bleClient = SimpleBleClient()
    bleClient.setScanCallback(myScanCallback)
    # TODO: NOTIFICATIONS ARE NOT SUPPORTED YET
    # bleClient.setNotificationCallback(myNotificationCollback)

    # Error handling to detect Keyboard interrupt (Ctrl+C)
    # Loop to ensure we can survive connection drops
    while(not bleClient.isConnected()):
        try:
            # Search for 2 seconds and return a device of interest if found.
            # Internally this makes a call to bleClient.scan(timeout), thus
            # triggering the scan callback method when nearby devices are detected
            device = bleClient.searchDevice(name="MyESP32", timeout=2)
            if(device is not None):
                # If the device was found print out it's info
                print("Found device!!")
                device.printInfo()

                # Proceed to connect to the device
                print("Proceeding to connect....")
                if(bleClient.connect(device)):

                    # Have a peek at the services provided by the device
                    services = device.getServices()
                    for service in services:
                        print("Service ["+str(service.uuid)+"]")

                    # Check to see if the device provides a characteristic with the
                    # desired UUID
                    counter = bleClient.getCharacteristics(
                        uuids=[Characteristic_UUID])[0]
                    if(counter):
                        # If it does, then we proceed to read its value every second
                        while(True):
                            # Error handling ensures that we can survive from
                            # potential connection drops
                            try:
                                # Read the data as bytes and convert to string
                                data_bytes = bleClient.readCharacteristic(
                                    counter)
                                data_str = "".join(map(chr, data_bytes))

                                # Now print the data and wait for a second
                                print("Data: " + data_str)
                                time.sleep(1.0)
                            except BTLEException as e:
                                # If we get disconnected from the device, keep
                                # looping until we have reconnected
                                if(e.code == BTLEException.DISCONNECTED):
                                    bleClient.disconnect()
                                    print(
                                        "Connection to BLE device has been lost!")
                                    break
                                    # while(not bleClient.isConnected()):
                                    #     bleClient.connect(device)

                else:
                    print("Could not connect to device! Retrying in 3 sec...")
                    time.sleep(3.0)
            else:
                print("Device not found! Retrying in 3 sec...")
                time.sleep(3.0)
        except BTLEException as e:
            # If we get disconnected from the device, keep
            # looping until we have reconnected
            if(e.code == BTLEException.DISCONNECTED):
                bleClient.disconnect()
                print(
                    "Connection to BLE device has been lost!")
                break
        except KeyboardInterrupt as e:
            # Detect keyboard interrupt and close down
            # bleClient gracefully
            bleClient.disconnect()
            raise e
