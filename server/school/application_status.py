class ApplicationStatus:
    CREATED = 0
    RELEASED = 1
    GATHERED = 2

    status_text = {
        CREATED: 'Заявка создана',
        RELEASED: 'Ребёнок выходит',
        GATHERED: 'Ребёнок забран',
    }

    @staticmethod
    def valid(status):
        return status in [ApplicationStatus.CREATED, ApplicationStatus.RELEASED, ApplicationStatus.GATHERED]

    @staticmethod
    def get_text(status):
        return ApplicationStatus.status_text[status] or '-'
