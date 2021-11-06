from datetime import datetime

from server.school.application_status import ApplicationStatus


class ApplicationUtils:
    @staticmethod
    def get_date(app):
        if app == '':
            return ''
        return datetime.fromisoformat(app['date']).strftime('%H:%M')

    @staticmethod
    def get_text(app):
        if app == '':
            return '-'
        return ApplicationStatus.get_text(app['status'])