import xml.etree.ElementTree as ET
import pandas as pd


def parse_siplace_xml(xml_file):

    tree = ET.parse(xml_file)
    root = tree.getroot()

    namespace = {
        "ns": "http://tempuri.org/ExportDsSetup.xsd"
    }

    rows = []

    for machine in root.findall(".//ns:Machine", namespace):

        machine_name = machine.find(
            "ns:MachineName",
            namespace
        ).text

        for table in machine.findall(
            "ns:Table",
            namespace
        ):

            table_nr = table.find(
                "ns:TableNr",
                namespace
            ).text

            location = table.find(
                "ns:TableLocationName",
                namespace
            ).text

            for feeder in table.findall(
                "ns:Feeder",
                namespace
            ):

                track = feeder.find(
                    "ns:TrackNr",
                    namespace
                ).text

                for division in feeder.findall(
                    "ns:Division",
                    namespace
                ):

                    div_nr = division.find(
                        "ns:DivisionNr",
                        namespace
                    ).text

                    component = division.find(
                        "ns:Component",
                        namespace
                    )

                    component_name = ""

                    if component is not None:
                        component_name = component.text

                    if not component_name:
                        component_name = "EMPTY"

                    rows.append(
                        {
                            "Machine": machine_name,
                            "Table": table_nr,
                            "Location": location,
                            "Track": track,
                            "Division": div_nr,
                            "Component": component_name
                        }
                    )

    return pd.DataFrame(rows)