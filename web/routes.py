import urllib.parse
from flask import render_template, url_for, request, make_response, redirect
from web import app, database
from web.models import Signatures
import web.utils as utils


@app.route('/')
def index():
    """
    home, where my ugly code should have stayed.
    """
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    """
    we need to pull stats on signature table/tactics and return to template
    """
    total = Signatures.query.count()
<<<<<<< HEAD
    tags = len(utils.get_tags())
    tactics = utils.get_tactics()

    return render_template('dashboard.html', query_count=total, tag_count=tags, tactic_names=list(tactics.keys()), tactic_counts=list(tactics.values()))
=======
    tactics = utils.get_tactics()
    tags = len(utils.get_tags())
    
    return render_template('dashboard.html', total=total, tactics=tactics, tags=tags)
>>>>>>> 6cf64079aaf09750488b91b2fce52a174cadb249


@app.route('/tactic/<tactic_name>')
def tactic(tactic_name):
    """
    Get all queries for specified tactic and pass to template
    """
    queries = Signatures.query.filter(Signatures.tactic.contains(tactic_name)).order_by(Signatures.title)
    return render_template('tactic.html', tactic=tactic_name, queries=queries)


@app.route('/tags')
def tags():
    """
    Load all tags from database and pass to template
    """
    results = utils.get_tags()
    per_group = 5
    groups = [results[i * per_group:(i + 1) * per_group] for i in range((len(results) + per_group - 1) // per_group)]
    return render_template('tags.html', tag_groups=groups)


@app.route('/tag/<tag_name>')
def tag(tag_name):
    """
    List all queries with specified tag.
    """
    queries = Signatures.query.filter(Signatures.tags.contains(tag_name)).order_by(Signatures.title)
    return render_template('tag.html', tagname=tag_name, queries=queries)


@app.route('/query/<query_id>')
def query(query_id):
    """
    Load the query by id, parse list items, grab console cookie
    and pass it all to the template.
    """
    results = Signatures.query.get(query_id)

    console_address = request.cookies.get('console')
    if console_address:
        # URLEncode query before creating link for queries with regex.
        #
        # TODO:
        #   - validate console_address as a url, maybe test the connection and throw flash() alert
        query_params = urllib.parse.quote_plus(results.dvquery)
        console_link = "{}/dv?queryString={}".format(console_address, query_params)
    else:
        console_link = None

    false_positives = []
    if results.false_positives is not None:
        entry = results.false_positives.split(',')
        for value in entry:
            false_positives.append(value.strip())

    references = []
    if results.references is not None:
        entry = results.references.split(',')
        for value in entry:
            references.append(value.strip())

    tag_list = []
    if results.tags is not None:
        entry = results.tags.split(',')
        for value in entry:
            tag_list.append(value.strip())

    tactic_list = []
    if results.tactic is not None:
        entry = results.tactic.split(',')
        for value in entry:
            tactic_list.append(value.strip())

    if results.subtechnique == "None":
        results.subtechnique = ""

    return render_template('query.html', query=results, tactics=tactic_list,
                           false_positives=false_positives, tags=tag_list,
                           references=references, console_address=console_link)


@app.route('/setconsole', methods=['POST'])
def setconsole():
    """
    Set the console address in cookie and return to previous page
    """
    referrer = request.headers.get("Referer")
    address = request.form["consoleaddress"]
    resp = make_response(redirect(referrer))
    resp.set_cookie(
        "console",
        value=address,
        httponly=False
    )
    return resp
