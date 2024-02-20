import re

class CVEclassifier:
    def __init__(self):
         self.keyword_mapping = {
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
            "iPhone": "M",
            "pc": "P",
            "laptop": "P",
            "computing": "P",
            "server": "P",
            "printer": "A",
            "copy machine": "A",
            "storage": "A",
            "multimedia": "A",
        }
        

    def cpe_contient_h(self, cve):
        cpe_regex = re.compile(r'cpe:[^:]*:h')
        for configuration in cve.get('configurations', []):
            for node in configuration.get('nodes', []):
                for cpe in node.get('cpeMatch', []):
                    criteria = cpe.get('criteria', '')
                    if cpe_regex.search(criteria):
                        return True
        return False
    
    def classify_cve(self,cve_description):        
        for keyword, category in self.keyword_mapping.items():
            if keyword in cve_description:
                return category
        return None
    
    def classify_all_cves(self,data):
        cves_to_insert = []
        for cve in data:
            if self.cpe_contient_h(cve):
                cve_description = cve["descriptions"][0]['value']
                category = self.classify_cve(cve_description)
                if category:
                    cve["category"] = category
            cves_to_insert.append(cve)
        return cves_to_insert