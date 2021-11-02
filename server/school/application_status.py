class ApplicationStatus:
    CREATED = 0
    RELEASED = 1
    GATHERED = 2

    @staticmethod
    def valid(status):
        return status in [ApplicationStatus.CREATED, ApplicationStatus.RELEASED, ApplicationStatus.GATHERED]