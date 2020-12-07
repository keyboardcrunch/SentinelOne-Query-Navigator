#!/usr/bin/python3
import os
import argparse
from web.models import Signatures
from web import database, metadata
from web.utils import load_signatures, query_folder


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="S1QN Management Script")
    p.add_argument('-rd',
                   '--reload-database',
                   action='store_true',
                   help='Reload signatures in database.')

    p.add_argument('-us',
                   '--update-sigs',
                   action='store_true',
                   help='Update signature files.')

    args = p.parse_args()

    if args.update_sigs:
        print("Refreshing signature repository and loading new signatures only...")
        # need to git pull
        load_signatures()

    if args.reload_database:
        print("Reloading database...")
        database.session.execute(database.table("Signatures").delete())
        load_signatures()
        print("Complete!")
