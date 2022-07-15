import grpc
from pet.v1 import pet_pb2
from pet.v1 import pet_pb2_grpc

from concurrent import futures
import logging

a = pet_pb2.Pet(pet_type=1, pet_id='1', name='first')  # 向数据库预添加的数据
max_id = 1  # 记录已使用过的最大编号
database = [a]  # 存放所有宠物数据的数据库


class Petstore(pet_pb2_grpc.PetStoreServiceServicer):
    # GetPet: 顺序查找id相同的宠物，有则返回，没有则返回一个空的Pet对象
    def GetPet(self, request, context):
        global database
        for i in database:
            if i.pet_id == request.pet_id:
                return pet_pb2.GetPetResponse(pet=i)
        return pet_pb2.GetPetResponse()

    # PutPet: 先查看待添加宠物是否已在数据库中，有则直接返回，否则追加到结尾，新宠物的id是max_id+1
    def PutPet(self, request, context):
        global max_id, database
        for i in database:
            if i.pet_type == request.pet_type and i.name == request.name:
                return pet_pb2.PutPetResponse(pet=i)
        max_id += 1
        new_pet = pet_pb2.Pet(pet_type=request.pet_type, pet_id=str(max_id), name=request.name)
        database.append(new_pet)
        return pet_pb2.PutPetResponse(pet=new_pet)

    # DeletePet: 顺序查找id相同的宠物，将其删除
    def DeletePet(self, request, context):
        global database
        for i in database:
            if i.pet_id == request.pet_id:
                database.remove(i)
                return pet_pb2.DeletePetResponse()
        return pet_pb2.DeletePetResponse()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pet_pb2_grpc.add_PetStoreServiceServicer_to_server(Petstore(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
