from app import create_app, db
from app.models.user import User
from app.models.listing import Listing

app = create_app()

sample_users = [
    {
        "name": "Amira",
        "email": "amira@example.com",
        "location": "Subang Jaya",
        "university": "Taylor's University",
        "password": "password123",
    },
    {
        "name": "Daniel",
        "email": "daniel@example.com",
        "location": "Sunway",
        "university": "Monash University Malaysia",
        "password": "password123",
    },
    {
        "name": "Lina",
        "email": "lina@example.com",
        "location": "Petaling Jaya",
        "university": "University of Malaya",
        "password": "password123",
    },
]

sample_listings = [
    {
        "title": "IKEA Study Desk",
        "description": "Sturdy desk in great condition.",
        "price": 120.0,
        "category": "Furniture",
        "condition": "Good",
        "location": "Subang Jaya",
        "university": "Taylor's University",
        "departure_date": "2026-07-20",
        "free": False,
        "image_url": "https://images.unsplash.com/photo-1541558869434-2840d308329a",
        "seller_email": "amira@example.com",
    },
    {
        "title": "MacBook Air M1",
        "description": "Lightly used for coding and assignments.",
        "price": 3200.0,
        "category": "Electronics",
        "condition": "Like New",
        "location": "Subang Jaya",
        "university": "Taylor's University",
        "departure_date": "2026-07-12",
        "free": False,
        "image_url": "https://images.unsplash.com/photo-1517336714739-489689fd1ca8",
        "seller_email": "amira@example.com",
    },
    {
        "title": "PS4 Console",
        "description": "Includes controller and FIFA 24.",
        "price": 900.0,
        "category": "Gaming",
        "condition": "Good",
        "location": "Petaling Jaya",
        "university": "University of Malaya",
        "departure_date": "2026-06-18",
        "free": False,
        "image_url": "https://images.unsplash.com/photo-1486401899868-0e435ed85128",
        "seller_email": "lina@example.com",
    },
    {
        "title": "Mechanical Keyboard",
        "description": "RGB keyboard with blue switches.",
        "price": 180.0,
        "category": "Gaming",
        "condition": "Like New",
        "location": "Sunway",
        "university": "Monash University Malaysia",
        "departure_date": "2026-06-20",
        "free": False,
        "image_url": "https://images.unsplash.com/photo-1511467687858-23d96c32e4ae",
        "seller_email": "daniel@example.com",
    },
    {
        "title": "Air Fryer",
        "description": "Barely used, still works perfectly.",
        "price": 110.0,
        "category": "Kitchen",
        "condition": "Good",
        "location": "Sunway",
        "university": "Monash University Malaysia",
        "departure_date": "2026-07-02",
        "free": False,
        "image_url": "https://images.unsplash.com/photo-1585515656973-94c94d9a0ef4",
        "seller_email": "daniel@example.com",
    },
]

def seed():
    with app.app_context():

        added_users = 0

        for user_data in sample_users:

            existing_user = User.query.filter_by(
                email=user_data["email"]
            ).first()

            if existing_user:
                continue

            user = User(
                name=user_data["name"],
                email=user_data["email"],
                location=user_data["location"],
                university=user_data["university"],
            )

            user.set_password(user_data["password"])

            db.session.add(user)
            added_users += 1

        db.session.commit()

        added_listings = 0

        for listing_data in sample_listings:

            seller = User.query.filter_by(
                email=listing_data["seller_email"]
            ).first()

            if not seller:
                continue

            existing_listing = Listing.query.filter_by(
                title=listing_data["title"],
                seller_id=seller.id
            ).first()

            if existing_listing:
                continue

            listing = Listing(
                title=listing_data["title"],
                description=listing_data["description"],
                price=listing_data["price"],
                category=listing_data["category"],
                condition=listing_data["condition"],
                location=listing_data["location"],
                university=listing_data["university"],
                departure_date=listing_data["departure_date"],
                free=listing_data["free"],
                image_url=listing_data["image_url"],
                seller_id=seller.id,
            )

            db.session.add(listing)
            added_listings += 1

        db.session.commit()

        print(
            f"Seed complete: {added_users} user(s) added, "
            f"{added_listings} listing(s) added."
        )

if __name__ == "__main__":
    seed()