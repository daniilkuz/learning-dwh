from fastapi.testclient import TestClient
from app.main import app

# testClient = TestClient(app)

# @pytest.fixture(scope="session")
# def client():
#     print("calling client()")
#     with TestClient(app) as session:
#         yield session
    
#     print("finished client()")

# @pytest.fixture(scope="function")
# def client():
#     return testClient

def test_create_get_items(client):
    page = 1
    page_size = 10
    response = client.get(f"/items?page={page}&page_size={page_size}")
    assert response.status_code == 200
    response_json = response.json()
    total = response_json['total']    

    price = -19
    amount = 10
    name = "Компьютер"
    response = client.post("/admin/items", json={
        "price": price,
        "amount": amount,
        "name": name
    })
    
    assert response.status_code==422

    price = 10
    response = client.post("/admin/items", json={
        "price": price,
        "amount": amount,
        "name": name
        })
    assert response.status_code==201, f"Error. Response body: {response.json()}"
    response_json = response.json()
    assert response_json['price'] == price and response_json['amount'] == amount

    # # тест ниже нужно доработать, т.к. нет гарантии, что запрашиваемый элемент будет последним в списке
    # total = total + 1
    # page_size = 1
    # page = total
    # response = client.get(f"/items?page={page}&page_size={page_size}")
    # assert response.status_code == 200, f"Error. Response body: {response.json()}"
    # response_json = response.json()
    # assert total == response_json['total'], "total amount is not correct"
    # assert response_json['items'][0]['price'] == price
    # assert response_json['items'][0]['amount'] == amount
    
# def test_example():
#     assert True

def test_create_delete_items(client):
    price = 23
    amount = 102
    name = "Наушники"
    response = client.post("/admin/items", json={
        "price": price,
        "amount": amount,
        "name": name
        })
    assert response.status_code==201, f"Error. Response body: {response.json()}"

    response_json = response.json()
    assert response_json['price'] == price and response_json['amount'] == amount
    
    id = response_json['id']
    not_valid_id = id+1

    response = client.delete(f"/admin/items/{not_valid_id}")
    assert response.status_code == 404

    response = client.delete(f"/admin/items/{id}")
    assert response.status_code == 204, f"Error. Response body: {response.json()}"
    
    response = client.delete(f"/admin/items/{id}")
    assert response.status_code == 404, f"Error. Response body: {response.json()}"
    
def test_create_get_orders(client):
    page = 1
    page_size = 10
    response = client.get(f"/orders?page={page}&page_size={page_size}")
    assert response.status_code == 200
    response_json = response.json()
    total = response_json['total']

    response = client.post("/orders")
    assert response.status_code == 201, f"Error. Response body: {response.json()}"
    response_json = response.json()
    assert response_json['user_id'] == 1
    assert response_json['status'] == 'PENDING'

    id = response_json['id']
    
    response = client.get(f"/orders/{id}")
    response_json = response.json()
    assert response_json['user_id'] == 1
    assert response_json['status'] == 'PENDING'
    assert response_json['id']==id

    # # тест ниже нужно доработать, т.к. нет гарантии, что запрашиваемый элемент будет последним в списке
    # total = total + 1
    # page_size = 1
    # page = total
    # response = client.get(f"/orders?page={page}&page_size={page_size}")
    # assert response.status_code == 200, f"Error. Response body: {response.json()}"
    # response_json = response.json()
    # assert total == response_json['total'], "total amount is not correct"
    # assert response_json['orders'][0]['id'] == id
    # assert response_json['orders'][0]['status'] == "PENDING"

def test_create_delete_orders(client):
    response = client.post("/orders")
    assert response.status_code==201, f"Error. Response body: {response.json()}"

    response_json = response.json()
    id = response_json['id']
    not_valid_id = id+1
    response = client.delete(f"/orders/{not_valid_id}")
    assert response.status_code == 404

    response = client.delete(f"/orders/{id}")
    assert response.status_code == 204, f"Error. Response body: {response.json()}"
    
    response = client.delete(f"/orders/{id}")
    assert response.status_code == 404, f"Error. Response body: {response.json()}"


def test_order_items(client):
    price = 19
    amount = 10
    name = "Компьютер"
    response = client.post("/admin/items", json={
        "price": price,
        "amount": amount,
        "name": name
        })
    
    assert response.status_code==201
    item_id = response.json()['id']
    
    response = client.post("/orders")
    assert response.status_code == 201, f"Error. Response body: {response.json()}"

    order_id = response.json()['id']

    not_valid_order_id = order_id+1
    response = client.get(f"/orders/{not_valid_order_id}/items")
    assert response.status_code == 404, f"Error. Response body: {response.json()}"
    
    response = client.get(f"/orders/{order_id}/items")
    assert response.status_code == 200, f"Error. Response body: {response.json()}"
    response_json = response.json()
    assert response_json['items']==[]

    amount = 20
    response = client.post(f"/orders/{order_id}/items", json={
        "item_id": item_id,
        "amount": amount
    })
    assert response.status_code == 201, f"Error. Response body: {response.json()}"
    response_json = response.json()

    response = client.post(f"/orders/{order_id}/items", json={
        "item_id": item_id,
        "amount": amount
    })
    assert response.status_code == 409, f"Error. Response body: {response.json()}"

    response = client.post("/admin/items", json={
        "price": price,
        "amount": amount,
        "name": name
        })
    
    item_id = response.json()['id']

    response = client.post(f"/orders/{order_id}/items", json={
            "item_id": item_id,
            "amount": amount
       })
    assert response.status_code == 201, f"Error. Response body: {response.json()}"

    response = client.get(f"/orders/{order_id}/items")
    assert response.status_code == 200, f"Error. Response body: {response.json()}"
    response_json  = response.json()
    assert len(response_json['items'])==2
    
    ### try remove an item from items
    response = client.delete(f"/admin/items/{item_id}")
    assert response.status_code == 409, f"Error. Response body: {response.json()}"
    
    ### remove the item from the order first
    response = client.delete(f"/orders/{order_id}/items/{item_id}")
    assert response.status_code == 204, f"Error. Response body: {response.json()}"

    ### chech that the item has been removed from the order
    response = client.get(f"/orders/{order_id}/items")
    assert response.status_code == 200, f"Error. Response body: {response.json()}"
    response_json  = response.json()
    assert len(response_json['items'])==1

    ### try remove an item from items
    response = client.delete(f"/admin/items/{item_id}")
    assert response.status_code == 204, f"Error. Response body: {response.json()}"