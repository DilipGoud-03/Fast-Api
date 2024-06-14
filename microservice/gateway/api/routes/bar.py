from fastapi import APIRouter
from schema.restaurant import OrderCreate
from api.dependencies.grpc.bar import BarClient

router = APIRouter()
client = BarClient()

@router.post( "",  status_code=201,  name="create_order")
def create_order(  
    order_create: OrderCreate ):
    response =  client.get_order(order=order_create.drink)
    return response