import xml.etree.cElementTree as ET
from xml.dom import minidom
from xml.etree.ElementTree import parse, Element


def read_xml(name):
    file_xml = minidom.parse(name)
    return file_xml


def xml_consult(vendor, model, softversion):
    try:
        file_xml = read_xml('datamodel.xml')
        docs = file_xml.getElementsByTagName('cm_model')

        for doc in docs:
            vendor_xml = doc.getElementsByTagName(
                'vendor')[0].firstChild.data.strip()
            model_xml = doc.getElementsByTagName(
                'model')[0].firstChild.data.strip()
            softversion_xml = doc.getElementsByTagName(
                'softversion')[0].firstChild.data.strip()

            if (vendor == vendor_xml or model == model_xml or softversion == softversion_xml):
                if (vendor == vendor_xml and model == model_xml and softversion == softversion_xml):
                    print(
                        'Todos los datos correspondientes a la información de los cablemodems se encontraban registrados')
                elif (vendor == vendor_xml):
                    print(
                        'La información "vendor" del cablemodem correspondiente ya se encontraba registrada, revisar modelo y softversion')
                elif (model == model_xml):
                    print(
                        'La información "modelo" del cablemodem correspondiente ya se encontraba registrada, revisar vendor y softversion')
                elif (softversion == softversion_xml):
                    print(
                        'La información "softversion" del cablemodem correspondiente ya se encontraba registrada, revisar vendor y modelo')

                in_xml = True
                break

            else:
                in_xml = False

        if in_xml == True:
            return in_xml, [(vendor_xml, model_xml, softversion_xml)]
        else:
            return in_xml, []

    except:
        """Archivo no existe, lo creamos"""

        root = ET.Element('cm_models')
        doc = ET.SubElement(root, 'cm_model')
        ET.SubElement(doc, "vendor").text = vendor
        ET.SubElement(doc, "model").text = model
        ET.SubElement(doc, "softversion").text = softversion

        file = ET.ElementTree(root)
        file.write("datamodel.xml")


def insert_xml(vendor, model, softversion):

    info = parse('datamodel.xml')
    root = info.getroot()
    doc = ET.SubElement(root, 'cm_model')
    ET.SubElement(doc, "vendor").text = vendor
    ET.SubElement(doc, "model").text = model
    ET.SubElement(doc, "softversion").text = softversion

    file = ET.ElementTree(root)
    file.write("datamodel.xml")

    records_xml = [(vendor, model, softversion)]
    return records_xml
