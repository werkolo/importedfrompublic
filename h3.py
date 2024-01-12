import psycopg2
import geojson
import os
import argparse
from h3 import h3 


def select_alter_table(input_geojson_file, table_name):
 
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )

    cursor = conn.cursor()

    cursor.execute('''SELECT Lat, Lon FROM {} ;'''.format(table_name))
    conn.commit()
    results = cursor.fetchall()
    print(results[0])
    print(results[1])
    #print(type(results[0][1]))

    cursor.execute('''ALTER TABLE {} ;'''.format(table_name))
    conn.commit()

  
    cursor.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='Uploader',
                    description='Uploads the isochrone geojson file to db', )

    parser.add_argument('-i', '--input-file', default=DEFAULT_DATA_FILEPATH)
    parser.add_argument('-t', '--table-name', default=DEFAULT_TABLENAME)

    args = parser.parse_args()
    
    h3_address = h3.geo_to_h3(37.3615593, -122.0553238, 9)

    with open(args.input_file, "r") as data_file:
        upload_data(data_file, args.table_name)
