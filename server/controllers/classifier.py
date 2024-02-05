from db.cve_collection import CveCollection


class CVEclassifier:
    def __init__(self):
        self.cve_collection= CveCollection()

    def classify_cve(self):
        classified_cves = []
        all_cves = self.cve_collection.get_all_cve()

        keyword_mapping = {
            "home": "H",
            "router": "H",
            "camera": "H",
            "appliance": "H",
            "scada": "S",
            "industrial": "S",
            "sensor": "S",
            "vehicle": "S",
            "medical": "S",
            "surveillance": "S",
            "enterprise": "E",
            "service provider": "E",
            "switch": "E",
            "networking": "E",
            "mobile": "M",
            "tablet": "M",
            "smart watch": "M",
            "portable": "M",
            "pc": "P",
            "laptop": "P",
            "computing": "P",
            "server": "P",
            "printer": "A",
            "copy machine": "A",
            "storage": "A",
            "multimedia": "A",
        }

        for cve_data in all_cves:
            cve_id = cve_data.get('_id', '')
            description_data = cve_data.get('descriptions', [])

            if description_data:
                description = description_data[0].get('value', '').lower()

                # Perform classification based on the CVE description
                category = next((category for keyword, category in keyword_mapping.items() if keyword in description), "Unclassified")

                if category != "Unclassified":
                    classified_cves.append({"cve_id": cve_id, "category": category})

        return classified_cves