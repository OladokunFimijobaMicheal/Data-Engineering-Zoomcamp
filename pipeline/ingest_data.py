#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm


# Database configuration
pg_user = "root"
pg_password = "root"
pg_host = "localhost"
pg_port = "5432"
pg_db = "ny_taxi"

# Dataset configuration
year = 2021
month = 1

target_table = "yellow_taxi_data"

url = (
    f"https://raw.githubusercontent.com/"
    f"OladokunFimijobaMicheal/Data-Engineering-Zoomcamp/main/"
    f"yellow_tripdata_{year}-{month:02d}.csv.gz"
)


# Column types
dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64",
    "airport_fee": "float64"
}


parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]


def run():

    chunksize = 100000

    # Create database connection
    engine = create_engine(
        f"postgresql+psycopg://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"
    )

    print("Downloading data...")

    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize,
        compression="gzip"
    )


    first = True

    for df_chunk in tqdm(df_iter):

        if first:
            # Create table schema
            df_chunk.head(0).to_sql(
                name=target_table,
                con=engine,
                if_exists="replace",
                index=False
            )

            first = False

            print("Table created")


        # Insert data
        df_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists="append",
            index=False
        )


        print(f"Inserted {len(df_chunk)} rows")


    print("Finished ingestion")


if __name__ == "__main__":
    run()