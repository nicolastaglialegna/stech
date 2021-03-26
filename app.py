from pysnmp.hlapi import *
import sys
import socket
import connection
import connection_xml


def check_ipv4(addres):
    try:
        if socket.inet_aton(addres):
            return True
    except socket.error:
        print('Invalid FORMAT IPV4')
        return False


def print_result(records):
    for row in records:
        print("Vendor: {0}, Model: {1}, softversion: {2}".format(
            row[0], row[1], row[2]))


class data(object):
    def __init__(self, vendor, model, softversion):
        self.vendor = vendor
        self.model = model
        self.softversion = softversion


ipv4 = check_ipv4(sys.argv[1])


if ipv4:

    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData('private'),
               UdpTransportTarget((sys.argv[1], 161)),
               ContextData(),
               ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))

    )

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            result = (varBinds[0].prettyPrint()).split("; ")
            info = data(result[1][8:], result[3][8:], result[4][7:-2])

            # VEMOS SI ESTA EN BBDD
            in_db, records_bd = connection.sql_consult(
                info.vendor, info.model, info.softversion)
            # TENEMOS QUE VER SI ESTA EN XML
            in_xml, records_xml = connection_xml.xml_consult(
                info.vendor, info.model, info.softversion)

            if (in_db == False and in_xml == False):
                if sys.argv[2] == 'db':
                    records_bd = connection.mysql_insert(
                        info.vendor, info.model, info.softversion)
                    in_db = True
                    print("DATOS CARGADOS EN BBDD")
                    print_result(records_bd)
                elif sys.argv[2] == 'file':
                    records_xml = connection_xml.insert_xml(
                        info.vendor, info.model, info.softversion)
                    in_xml = True
                    print("DATOS CARGADOS EN FILE")
                    print_result(records_xml)
                elif sys.argv[2] == "both":
                    records_bd = connection.mysql_insert(
                        info.vendor, info.model, info.softversion)
                    records_xml = connection_xml.insert_xml(
                        info.vendor, info.model, info.softversion)
                    in_db = True
                    in_xml = True
                    print("DATOS CARGADOS EN BBDD Y FILE")
                    print_result(records_bd)
            else:
                if (in_db == True and in_xml == False):
                    print("Dato cargado previamente en BBDD")
                    print_result(records_bd)
                if (in_xml == True and in_db == False):
                    print("Dato cargado previamente en FILE")
                    print_result(records_xml)
                if (in_db == True and in_xml == True):
                    print("Dato cargado previamente en BBDD y FILE")
                    print_result(records_bd)
