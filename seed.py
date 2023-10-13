from app import db  # Import your SQLAlchemy db object from your Flask application
from models import Hero, Power, HeroPower

# Create sample data for heroes, powers, and hero_power relationships
def seed_database():
    # Create heroes
    hero1 = Hero(name="Superman", super_power="Flight")
    hero2 = Hero(name="Batman", super_power="Intelligence")

    # Create powers
    power1 = Power(name="Super Strength", description="Incredibly strong")
    power2 = Power(name="Utility Belt", description="Contains gadgets and tools")

    # Add objects to the session and commit to the database
    db.session.add(hero1)
    db.session.add(hero2)
    db.session.add(power1)
    db.session.add(power2)
    db.session.commit()

    # Create hero_power relationships
    hero_power1 = HeroPower(hero=hero1, power=power1, strength="Strong")
    hero_power2 = HeroPower(hero=hero2, power=power2, strength="Average")

    # Add hero_power relationships to the session and commit
    db.session.add(hero_power1)
    db.session.add(hero_power2)
    db.session.commit()

if __name__ == "__main__":
    seed_database()

