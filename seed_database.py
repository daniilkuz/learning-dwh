import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Item, User, Order, OrderItem, OrderStatus
from config.database import create_tables
import os
from dotenv import load_dotenv


# Create database engine and session

load_dotenv()

random.seed(42)

# Получение параметров подключения из переменных окружения
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "fastapi_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
# SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://postgres:postgres@localhost:5432/fastapi_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False,  # при отладке тут нужен True, как сделать более гибко, чтобы во время отладки не приходилось вручную менять значения в коде?
)

Session = sessionmaker(bind=engine)
session = Session()


def create_sample_data():
    """Populate the database with sample data"""

    print("Creating sample data...")

    # Clear existing data (optional - be careful!)
    # Uncomment only if you want to start fresh
    # session.query(OrderItem).delete()
    # session.query(Order).delete()
    # session.query(Item).delete()
    # session.query(User).delete()

    create_tables()

    # Create sample items
    items_data = [
        {"name": "Laptop", "price": 999.99, "amount": 10},
        {"name": "Smartphone", "price": 699.99, "amount": 25},
        {"name": "Headphones", "price": 149.99, "amount": 50},
        {"name": "Keyboard", "price": 79.99, "amount": 30},
        {"name": "Mouse", "price": 29.99, "amount": 100},
        {"name": "Monitor", "price": 299.99, "amount": 15},
        {"name": "USB Cable", "price": 9.99, "amount": 200},
        {"name": "Power Bank", "price": 49.99, "amount": 40},
        {"name": "Tablet", "price": 399.99, "amount": 20},
        {"name": "Smart Watch", "price": 199.99, "amount": 35},
        {"name": "Gaming Console", "price": 499.99, "amount": 8},
        {"name": "Wireless Earbuds", "price": 129.99, "amount": 60},
        {"name": "External SSD", "price": 89.99, "amount": 45},
        {"name": "Webcam", "price": 69.99, "amount": 30},
        {"name": "Desk Lamp", "price": 39.99, "amount": 75},
    ]

    items = []
    for item_data in items_data:
        item = Item(
            name=item_data["name"], price=item_data["price"], amount=item_data["amount"]
        )
        items.append(item)
        session.add(item)

    session.commit()
    print(f"Created {len(items)} items")

    # Create sample users
    users_data = [
        {
            "username": "john_doe",
            "email": "john.doe@example.com",
            "phone": "+1234567890",
            "name": "John",
            "surename": "Doe",
            "patronymic": "Michael",
        },
        {
            "username": "jane_smith",
            "email": "jane.smith@example.com",
            "phone": "+0987654321",
            "name": "Jane",
            "surename": "Smith",
            "patronymic": "Elizabeth",
        },
        {
            "username": "alex_wong",
            "email": "alex.wong@example.com",
            "phone": "+1122334455",
            "name": "Alex",
            "surename": "Wong",
            "patronymic": "Chen",
        },
        {
            "username": "maria_garcia",
            "email": "maria.garcia@example.com",
            "phone": "+5566778899",
            "name": "Maria",
            "surename": "Garcia",
            "patronymic": "Isabella",
        },
        {
            "username": "robert_kim",
            "email": "robert.kim@example.com",
            "phone": "+6677889900",
            "name": "Robert",
            "surename": "Kim",
            "patronymic": "James",
        },
    ]

    users = []
    for user_data in users_data:
        user = User(
            username=user_data["username"],
            email=user_data["email"],
            phone=user_data["phone"],
            name=user_data["name"],
            surename=user_data["surename"],
            patronymic=user_data["patronymic"],
        )
        users.append(user)
        session.add(user)

    session.commit()
    print(f"Created {len(users)} users")

    # Create sample orders
    orders = []
    statuses = [OrderStatus.PENDING, OrderStatus.FINISHED, OrderStatus.CANCELLED]

    for _ in range(20):  # Create 20 orders
        user = random.choice(users)
        order = Order(user_id=user.id, status=random.choice(statuses))
        orders.append(order)
        session.add(order)

    session.commit()
    print(f"Created {len(orders)} orders")

    # Create order items (associations between orders and items)
    order_items_created = 0

    for order in orders:
        # Each order gets 1-5 random items
        num_items = random.randint(1, 5)
        selected_items = random.sample(items, min(num_items, len(items)))

        for item in selected_items:
            # Random amount between 1 and 5
            amount = random.randint(1, 5)

            order_item = OrderItem(order_id=order.id, item_id=item.id, amount=amount)
            session.add(order_item)
            order_items_created += 1

            # Also update the relationships
            # if order not in item.orders:
            #     item.orders.append(order)
            # if item not in order.items:
            #     order.items.append(item)

    session.commit()
    print(f"Created {order_items_created} order items")

    print("\nSample data created successfully!")

    # Display summary
    print("\n=== Database Summary ===")
    print(f"Total Users: {session.query(User).count()}")
    print(f"Total Items: {session.query(Item).count()}")
    print(f"Total Orders: {session.query(Order).count()}")
    print(f"Total Order Items: {session.query(OrderItem).count()}")

    # Show some example data
    print("\n=== Sample Order Details ===")
    sample_order = session.query(Order).first()
    if sample_order:
        print(f"Order ID: {sample_order.id}")
        print(f"User: {sample_order.user.name} {sample_order.user.surename}")
        print(f"Status: {sample_order.status}")
        print("Items in this order:")
        for order_item in (
            session.query(OrderItem).filter_by(order_id=sample_order.id).all()
        ):
            item = session.query(Item).filter_by(id=order_item.item_id).first()
            if item:
                print(
                    f"  - {item.name}: {order_item.amount} pcs × ${item.price} = ${order_item.amount * item.price:.2f}"
                )


def test_relationships():
    """Test that relationships are working correctly"""
    print("\n=== Testing Relationships ===")

    # Get a user and show their orders
    user = session.query(User).first()
    if user:
        print(f"\nUser: {user.username}")
        print(f"Number of orders: {len(user.orders)}")
        for order in user.orders:
            print(f"  Order #{order.id}: {order.status}")
            print(f"  Items: {[item.name for item in order.items]}")

    # Get an item and show which orders include it
    item = session.query(Item).first()
    if item:
        print(f"\nItem: {item.name}")
        print(f"Price: ${item.price}")
        print(f"Stock: {item.amount}")
        print(f"Number of orders containing this item: {len(item.orders)}")


if __name__ == "__main__":
    try:
        create_sample_data()
        test_relationships()
        print("\nDatabase population completed successfully!")
    except Exception as e:
        session.rollback()
        print(f"Error occurred: {e}")
        raise
    finally:
        session.close()
