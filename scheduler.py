import schedule

from controllers.import_controller import ImportController


class Scheduler(object):

    def run(self):
        schedule.every(2).hours.do(ImportController().update_cves())
