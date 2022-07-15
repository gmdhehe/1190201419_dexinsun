import grpc
from pet.v1 import pet_pb2
from pet.v1 import pet_pb2_grpc

from concurrent import futures
import logging

"""
客户端测试流程:首先查找预添加数据，然后向数据库中添加数据，查找新添加的宠物，最后将添加数据删除，再查找一次看是否删除成功
"""

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = pet_pb2_grpc.PetStoreServiceStub(channel)

        # 查找预添加数据，未查到对象时接收空Pet，提示没有该宠物
        response1 = stub.GetPet(pet_pb2.GetPetRequest(pet_id='1'))
        if response1.pet == pet_pb2.Pet():
            print("No such pet id in database.")
        else:
            print("Greeter client received:")
            print(response1.pet)

        # 添加宠物数据
        response2 = stub.PutPet(pet_pb2.PutPetRequest(pet_type=2, name='second'))
        print("successfully put")
        print(response2.pet)

        # 查找刚添加的数据看是否添加成功
        response3 = stub.GetPet(pet_pb2.GetPetRequest(pet_id='2'))
        if response3.pet == pet_pb2.Pet():
            print("No such pet in database.")
        else:
            print("Greeter client received:")
            print(response3.pet)

        # 删除新添加数据
        response4 = stub.DeletePet(pet_pb2.DeletePetRequest(pet_id='2'))

        # 再次查找，看是否删除成功
        response3 = stub.GetPet(pet_pb2.GetPetRequest(pet_id='2'))
        if response3.pet == pet_pb2.Pet():
            print("No such pet in database.")
        else:
            print("Greeter client received:")
            print(response3.pet)


if __name__ == '__main__':
    logging.basicConfig()
    run()