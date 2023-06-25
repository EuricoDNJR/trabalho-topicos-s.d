from prisma import Prisma


class RDSConnector:
    def __init__(self):
        self.prisma = Prisma()

    async def connect(self):
        await self.prisma.connect()

    async def disconnect(self):
        await self.prisma.disconnect()

    async def create_data(self, data: dict):
        return await self.prisma.test.create(data)

    async def get_device(self, id: int):
        return await self.prisma.device.find_first(
            where={'id': id}
        )
    # async def update_recorded_audio_status(self, id: int, status: str):
    #     return await self.prisma.recordedaudio.update(
    #         where={'id': id},
    #         data={'status': status}
    #     )

    # async def create_scenario_predict(self, data: dict):
    #     return await self.prisma.scenariopredict.create(data)
    
    # async def create_user(self, data: dict):
    #     return await self.prisma.user.create(data)

    # async def create_device(self, device_name: str):
    #     return await self.prisma.device.create({'deviceName': device_name})

    # async def get_device(self, device_name: str):
    #     return await self.prisma.device.find_first(
    #         where={'deviceName': device_name}
    #     )

    # async def get_hives(self, device_name: str):
    #     return await self.prisma.device.find_first(
    #         where={'deviceName': device_name},
    #         include={
    #             'RecordedAudio': {
    #                 'include': {
    #                     'scenariosPredict': True
    #                 }
    #             }
    #         }
    #     )
