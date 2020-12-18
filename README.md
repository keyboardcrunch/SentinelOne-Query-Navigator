# SentinelOne Query Navigator

A Python Flask based web application for loading the [SentinelOne-Queries](https://github.com/keyboardcrunch/sentinelone-queries) repository into a browseable database, where the queries can be easily navigated or directly queried against your own SentinelOne console with one click.

This project was created to solve problems with sharing, storing and using developed queries. Often times you'll want to run a query adhoc but not store it in the console, and sometimes storing and loading queries within console is cumbersome, so this provides a means to review and run queries from outside the console.

## Signatures / Queries
As stated above, the [SentinelOne-Queries](https://github.com/keyboardcrunch/sentinelone-queries) repository is the query-base, but any repositories can be added to the queries/ subfolder, as anything new in the queries/ folder will be loaded at runtime.

## Managing Signatures
A `manage.py` has been included for updating the keyboardcrunch query repository ( ```python manage.py --update-sigs``` ) or forcefully reloading all signatures within the Signatures table ( ```python manage.py --reload-database``` ).

## Running Queries
To run a query, first set your console address like `https://console.sentinelone.com` in the navigator. Then you will see the Query button on the query page, clicking it will automatically open a new browser tab passing the query to your SentinelOne console.

## Screenshots
![Main View](https://github.com/keyboardcrunch/SentinelOne-Query-Navigator/blob/main/screenshots/Main.png?raw=True)

![Tactic View](https://github.com/keyboardcrunch/SentinelOne-Query-Navigator/blob/main/screenshots/TacticView.png?raw=True)

![Query View](https://github.com/keyboardcrunch/SentinelOne-Query-Navigator/blob/main/screenshots/QueryView.png?raw=True)

## Getting Started
```
# Clone the repository
git clone --recurse-submodules -j8 git@github.com:keyboardcrunch/SentinelOne-Query-Navigator.git

# Install requirements
pip3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

# Run locally
./run.sh

# Run with uwsgi
uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app
```


## Contributions
Feel free to submit bug fixes, code clean-up, or additional features. For now this is just a fun personal project, but I'd like to see the community take it somewhere or help make it better. 

## TODO
- ~~Fix the template DOM sizing and layout~~
- ~~Add pagination to the /tactic/ view~~
- ~~Add a view for queries without Mitre information~~
- ~~Finish the index and dashboard pages~~
- App settings for auto-run of query and default timeframe
- Ability to refresh data without bumping row ID
- Views for technique
- Map Tactic to Mitre Tactic ID (maybe)
