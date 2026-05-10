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
        "description": "Sturdy desk in great condition, perfect for study or work from home.",
        "price": 120.0,
        "category": "Furniture",
        "condition": "Good",
        "location": "Subang Jaya",
        "university": "Taylor's University",
        "departure_date": "2026-07-20",
        "free": False,
        "image_url": "https://images.unsplash.com/photo-1541558869434-2840d308329a?auto=format&fit=crop&w=1200&q=80",
        "seller_email": "amira@example.com",
    },
    {
        "title": "Organic Chemistry Textbook",
        "description": "Used once, clean pages, excellent for final revisions.",
        "price": 35.0,
        "category": "Textbooks",
        "condition": "Like New",
        "location": "Sunway",
        "university": "Monash University Malaysia",
        "departure_date": "2026-06-30",
        "free": False,
        "image_url": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?auto=format&fit=crop&w=1200&q=80",
        "seller_email": "daniel@example.com",
    },
    {
        "title": "Free Microwave Oven",
        "description": "Working microwave, just needs a new home before I leave.",
        "price": 0.0,
        "category": "Electronics",
        "condition": "Fair",
        "location": "Petaling Jaya",
        "university": "University of Malaya",
        "departure_date": "2026-05-28",
        "free": True,
        "image_url": "https://images.unsplash.com/photo-1574269909862-7e1d70bb8078?auto=format&fit=crop&w=1200&q=80",
        "seller_email": "lina@example.com",
    },
    {
        "title": "Acoustic Guitar",
        "description": "Warm-sounding guitar with a few scratches, comes with a soft case.",
        "price": 80.0,
        "category": "Electronics",
        "condition": "Like New",
        "location": "Subang Jaya",
        "university": "Taylor's University",
        "departure_date": "2026-06-10",
        "free": False,
        "image_url": "https://images.unsplash.com/photo-1510915361894-db8b60106cb1?auto=format&fit=crop&w=1200&q=80",
        "seller_email": "amira@example.com",
    },
    {
        "title": "Second-hand Office Chair",
        "description": "Comfortable chair with lumbar support, great for long study sessions.",
        "price": 50.0,
        "category": "Furniture",
        "condition": "Good",
        "location": "Sunway",
        "university": "Monash University Malaysia",
        "departure_date": "2026-07-05",
        "free": False,
        "image_url": "https://images.unsplash.com/photo-1505797149-7f8b7c0e0f1f?auto=format&fit=crop&w=1200&q=80",
        "seller_email": "daniel@example.com",
    },
]


def seed():
    with app.app_context():
        added_users = 0
        for user_data in sample_users:
            existing_user = User.query.filter_by(email=user_data["email"]).first()
            if existing_user:
                if not existing_user.location:
                    existing_user.location = user_data["location"]
                if not existing_user.university:
                    existing_user.university = user_data["university"]
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
            seller = User.query.filter_by(email=listing_data["seller_email"]).first()
            if not seller:
                continue
            existing_listing = Listing.query.filter_by(
                title=listing_data["title"], seller_id=seller.id
            ).first()
            if existing_listing:
                # Keep existing records, but backfill image URLs for old seed data.
                if not existing_listing.location and listing_data["location"]:
                    existing_listing.location = listing_data["location"]
                if not existing_listing.university and listing_data["university"]:
                    existing_listing.university = listing_data["university"]
                if not existing_listing.image_url and listing_data["image_url"]:
                    existing_listing.image_url = listing_data["image_url"]
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
        print(f"Seed complete: {added_users} user(s) added, {added_listings} listing(s) added.")


if __name__ == "__main__":
    seed()
