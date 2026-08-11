from sqlalchemy import func, select

from app.db.engine import engine
from app.db.tables import embeddings


def main():

    with engine.connect() as connection:

        count = connection.execute(
            select(func.count())
            .select_from(embeddings)
        ).scalar_one()

    print()
    print("Embedding count:")
    print(count)


if __name__ == "__main__":
    main()