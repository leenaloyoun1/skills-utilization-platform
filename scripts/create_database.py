"""Create all PostgreSQL tables using SQLAlchemy Core."""

from app.db.engine import engine
from app.db.tables import metadata


def main():
    print("Creating database tables...")

    metadata.create_all(engine)

    print("Database tables created successfully.")


if __name__ == "__main__":
    main()