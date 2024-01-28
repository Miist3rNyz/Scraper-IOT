from importers.cve_importer import CveImporter


class ImportController(object):

    def populate_cve_collection(self) -> None:
        CveImporter().run_full_import()