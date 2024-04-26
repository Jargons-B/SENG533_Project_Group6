import random
import string
from datetime import datetime, timedelta

def generate_random_string(length, character_set=string.ascii_letters):
    return ''.join(random.choices(character_set, k=length))

def generate_random_url():
    return f"https://{generate_random_string(10)}.com/{generate_random_string(10)}"

def generate_random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)

def generate_random_document():
    """Generate a document with random data similar to Airbnb listing."""
    check_in_date = generate_random_date(datetime.now(), datetime.now() + timedelta(days=365))
    check_out_date = generate_random_date(check_in_date, check_in_date + timedelta(days=90))
    return {
        "name": generate_random_string(20, string.ascii_uppercase),
        "listing_url": generate_random_url(),
        "summary": generate_random_string(100),
        "space": generate_random_string(200),
        "description": generate_random_string(250),
        "neighborhood_overview": generate_random_string(150),
        "notes": generate_random_string(100),
        "transit": generate_random_string(100),
        "access": generate_random_string(100),
        "interaction": generate_random_string(100),
        "house_rules": "No smoking. No pets allowed. Please respect the neighbors.",
        "property_type": random.choice(["House", "Apartment", "Condominium", "Loft", "Townhouse"]),
        "room_type": random.choice(["Entire home/apt", "Private room", "Shared room"]),
        "bed_type": "Real Bed",
        "minimum_nights": random.randint(1, 10),
        "maximum_nights": random.randint(30, 365),
        "cancellation_policy": random.choice(["flexible", "moderate", "strict"]),
        "last_scraped": datetime.now().isoformat(),
        "calendar_last_scraped": datetime.now().isoformat(),
        "first_review": check_in_date.isoformat(),
        "last_review": check_out_date.isoformat(),
        "accommodates": random.randint(1, 10),
        "bedrooms": random.randint(1, 5),
        "beds": random.randint(1, 5),
        "number_of_reviews": random.randint(0, 100),
        "bathrooms": random.random() * 5,
        "amenities": ["Wifi", "Kitchen", "Iron", "Laptop friendly workspace"],
        "price": random.uniform(50, 500),
        "security_deposit": random.uniform(150, 300),
        "cleaning_fee": random.uniform(10, 100),
        "extra_people": random.uniform(5, 25),
        "guests_included": random.randint(1, 4),
        "images": {
            "thumbnail_url": "",
            "medium_url": "",
            "picture_url": generate_random_url(),
            "xl_picture_url": ""
        },
        "host": {
            "host_id": generate_random_string(10, string.digits),
            "host_url": generate_random_url(),
            "host_name": generate_random_string(15),
            "host_location": generate_random_string(30),
            "host_about": generate_random_string(200),
            "host_response_time": random.choice(["within an hour", "within a few hours", "within a day"]),
            "host_thumbnail_url": generate_random_url(),
            "host_picture_url": generate_random_url(),
            "host_neighbourhood": generate_random_string(15),
            "host_response_rate": random.randint(50, 100),
            "host_is_superhost": random.choice([True, False]),
            "host_has_profile_pic": random.choice([True, False]),
            "host_identity_verified": random.choice([True, False]),
            "host_listings_count": random.randint(1, 5),
            "host_total_listings_count": random.randint(1, 5)
        },
        "host_verifications": ["email", "phone", "government_id"],
        "address": {
            "street": generate_random_string(40),
            "suburb": generate_random_string(15),
            "government_area": generate_random_string(30),
            "market": generate_random_string(20),
            "country": "Country",
            "country_code": "US"
        },
        "location": {
            "type": "Point",
            "coordinates": [random.uniform(-180, 180), random.uniform(-90, 90)]
        },
        "availability": {
            "availability_30": random.randint(0, 30),
            "availability_60": random.randint(0, 60),
            "availability_90": random.randint(0, 90),
            "availability_365": random.randint(0, 365)
        },
        "review_scores": {
            "review_scores_accuracy": random.randint(1, 10),
            "review_scores_cleanliness": random.randint(1, 10),
            "review_scores_checkin": random.randint(1, 10),
            "review_scores_communication": random.randint(1, 10),
            "review_scores_location": random.randint(1, 10),
            "review_scores_value": random.randint(1, 10),
            "review_scores_rating": random.randint(20, 100)
        },
        "reviews": [
            {
                "_id": generate_random_string(10, string.digits),
                "date": check_in_date.isoformat(),
                "listing_id": generate_random_string(10, string.digits),
                "reviewer_id": generate_random_string(10, string.digits),
                "reviewer_name": generate_random_string(15),
                "comments": generate_random_string(250)
            }
        ]
    }

def generate_update_data():
    return {
        'name': generate_random_string(10),
        'summary': generate_random_string(50),
        'description': generate_random_string(100),
        'space': generate_random_string(100),
        'access': generate_random_string(50),
        'amenities': [generate_random_string(10) for _ in range(5)],
        'price': round(random.uniform(50, 200), 2),
        'bedrooms': random.randint(1, 5),
        'beds': random.randint(2, 2),
        'bathrooms': round(random.uniform(1, 3), 1),
    }

def random_document(collection):
    document = {
        'name': generate_random_string(10),
        'summary': generate_random_string(50),
        'price': round(random.uniform(50, 200), 2),
        'bedrooms': random.randint(1, 5)
    }
    collection.insert_one(document)