from prisma import Prisma


class RDSConnector:
    def __init__(self):
        self.prisma = Prisma()

    def connect(self):
        self.prisma.connect()

    def disconnect(self):
        self.prisma.disconnect()

    def create_data(self, data: dict):
        return self.prisma.test.create(data)

    def print_all(self: object) -> None:
        users = self.prisma.test.find_many()

        for user in users:
            print(user.id, user.iseven)

