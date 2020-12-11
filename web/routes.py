import urllib.parse
from flask import render_template, url_for, request, make_response, redirect
from web import app, database
from web.models import Signatures
import web.utils as utils

pagination_count = 20

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
    tags = len(utils.get_tags()) # TODO: Change to dict {tag:count} and create pie chart
    tactics = utils.get_tactics()

    return render_template('dashboard.html', query_count=total, tag_count=tags,
                           tactic_names=list(tactics.keys()), tactic_counts=list(tactics.values()))


@app.route('/all')
def allqueries():
    """
    All queries.
    """
    page = request.args.get('page', 1, type=int)
    results = Signatures.query.order_by(Signatures.title).paginate(
        page, pagination_count, False
    )
    next_url = url_for('allqueries', page=results.next_num) if results.has_next else None
    prev_url = url_for('allqueries', page=results.prev_num) if results.has_prev else None

    return render_template("query_list.html", title="All Queries", queries=results.items, next_url=next_url, prev_url=prev_url)


@app.route('/generics')
def generics():
    """
    Queries without Mitre data.
    """
    page = request.args.get('page', 1, type=int)
    results = Signatures.query.filter(Signatures.tactic == None ).order_by(Signatures.title).paginate(
        page, pagination_count, False
    )
    next_url = url_for('generics', page=results.next_num) if results.has_next else None
    prev_url = url_for('generics', page=results.prev_num) if results.has_prev else None
    return render_template('query_list.html', title="Generic Queries", queries=results.items, next_url=next_url, prev_url=prev_url)


@app.route('/tags')
def tags():
    """
    Load all tags from database, group them for pagination, return results to template.
    """
    all_tags = utils.get_tags()
    page = request.args.get('page', 0, type=int)
    group = [all_tags[i * pagination_count:(i + 1) * pagination_count] for i in range((len(all_tags) + pagination_count - 1) // pagination_count)]
    try:
        next_group = group[page + 1]
    except:
        next_group = None
    prev_group = page - 1
    next_url = url_for('tags', page=next_group) if next_group else None
    prev_url = url_for('tags', page=prev_group) if prev_group >= 0 else None
    return render_template('tags.html', tags=group[page], next_url=next_url, prev_url=prev_url)


@app.route('/tag/<tag_name>')
def tag(tag_name):
    """
    List all queries with specified tag. Sloppily uses 'contains' as tags column in db is comma separated list.
    Will want to change this in the future as it causes bad results. 
    """
    title = "Tag: {}".format(tag_name)
    page = request.args.get('page', 1, type=int)
    results = Signatures.query.filter(Signatures.tags.contains(tag_name)).order_by(Signatures.title).paginate(
        page, pagination_count, False
    )
    next_url = url_for('generics', page=results.next_num) if results.has_next else None
    prev_url = url_for('generics', page=results.prev_num) if results.has_prev else None
    return render_template('query_list.html', title=title, queries=results.items, next_url=next_url, prev_url=prev_url)


@app.route('/tactic/<tactic_name>')
def tactic(tactic_name):
    """
    Get all queries for specified tactic and pass to template
    """
    page = request.args.get('page', 1, type=int)
    results = Signatures.query.filter(Signatures.tactic.contains(tactic_name)).order_by(Signatures.title).paginate(
        page, pagination_count, False
    )
    next_url = url_for('tactic', tactic_name=tactic_name, page=results.next_num) if results.has_next else None
    prev_url = url_for('tactic', tactic_name=tactic_name, page=results.prev_num) if results.has_prev else None
    return render_template('query_list.html', title=tactic_name, queries=results.items, next_url=next_url, prev_url=prev_url)


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
