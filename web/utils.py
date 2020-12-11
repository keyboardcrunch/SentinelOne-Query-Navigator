import os
import yaml
from pathlib import Path
from web import app, database
from web.models import Signatures

query_folder = os.path.abspath("queries")

def get_tags():
    """
    Return a list of all tags from all signatures.
    """
    tags = []
    query = database.session.query(Signatures.tags.distinct().label("title"))
    results = [row.title for row in query.all()]
    for item in results:
        if item is not None:
            entry = item.split(',')
            for value in entry:
                if not value.strip() in tags:
                    tags.append(value.strip())
    return sorted(tags)


def get_tactics():
<<<<<<< HEAD
    """
    Load all tactics into a dictionary and return for later graphing.
    """
    collection = {}
=======
    collection = []
>>>>>>> 6cf64079aaf09750488b91b2fce52a174cadb249
    tactics = []
    query = database.session.query(Signatures.tactic.distinct().label("title"))
    results = [row.title for row in query.all()]
    for item in results:
        if item is not None:
            entry = item.split(',')
            for value in entry:
                if not value.strip() in tactics:
                    tactics.append(value.strip())
    for tactic in tactics:
        res = Signatures.query.filter(Signatures.tactic.contains(tactic)).count()
<<<<<<< HEAD
        obj = {
            tactic: res
        }
        collection.update(obj)
    return collection
=======
        print(res)
        obj = {
            "name": tactic,
            "count": res
        }
        collection.append(obj)
    return collection


def build_dashboard():
    dashboard = ""
    return dashboard
>>>>>>> 6cf64079aaf09750488b91b2fce52a174cadb249


def load_signatures():
    """
    Load signatures from query folder. Won't refresh data, only loads new
    content where there isn't a title conflict.
    """
    for sig_file in Path(query_folder).rglob('*.yml'):
        with open(sig_file) as s:
            try:
                signatures = yaml.load_all(s, Loader=yaml.FullLoader) # handle multi-signature files
                for signature in signatures:
                    if signature['false_positives'] and not isinstance(signature['false_positives'], type(None)):
                        false_pos = ",".join(signature['false_positives'])
                    else:
                        false_pos = None

                    if signature['tags'] and not isinstance(signature['tags'], type(None)):
                        tags = ",".join(signature['tags'])
                    else:
                        tags = None

                    try:
                        if signature['references'] and not isinstance(signature['references'], type(None)):
                            refs = ",".join(signature['references'])
                        else:
                            refs = None
                    except: # handle missing value entirely
                        refs = None
                    
                    # ensure subtechnique has padded zeros
                    subtech = str(signature['mitre']['subtechnique']).zfill(3)

                    try:
                        siggy = Signatures(title=signature['title'],
                                description=signature['description'],
                                author=signature['author'],
                                date=signature['date'],
                                modified=signature['modified'],
                                tactic=signature['mitre']['tactic'],
                                technique=signature['mitre']['technique'],
                                subtechnique=subtech,
                                operating_system=signature['operating_system'],
                                dvquery=signature['query'],
                                false_positives=false_pos,
                                tags=tags,
                                references=refs)
                        database.session.add(siggy)
                        database.session.commit()

                    except Exception as e:
                        database.session.rollback()
            except Exception as e:
                print("Error: {}\r\nSignature: {}".format(e, signature['title']))