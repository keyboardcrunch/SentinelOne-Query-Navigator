#!/usr/bin/python3
import os
import argparse
from git import Repo
from web.models import Signatures
from web import database, metadata
from web.utils import load_signatures, query_folder

base_dir = os.path.abspath(os.path.dirname(__file__))
keyboardcrunch_repo = os.path.join(base_dir, "queries/keyboardcrunch/")

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
        print("Refreshing keyboardcrunch signature repository... Only new content will be loaded.")
        repo = Repo(keyboardcrunch_repo)
        repo.remotes.origin.pull('main')
        load_signatures()

    elif args.reload_database:
        print("Reloading database...")
        database.session.execute(database.table("Signatures").delete())
        load_signatures()
        print("Complete!")

    else:
        p.print_help()