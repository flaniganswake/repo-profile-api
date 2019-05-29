""" Github/Bitbucket API routing
    flaniganswake@protonmail.com """
import flask
from app_impl.bitapi import BitbucketRepoAPIData
from app_impl.gitapi import GithubRepoAPIData

app = flask.Flask("user_profiles_api")


@app.errorhandler(404)
def not_found(_):
    ''' endpoint to 404 '''
    return flask.make_response(
        flask.jsonify({'Error': 'Not found'}), 404)


@app.route('/', methods=['GET'])
@app.route('/api/v1.0/', methods=['GET'])
def root():
    ''' endpoint to root API '''
    data = {
        "Repo queries for a user": {
            "Single": "/api/v1.0/repos/?user=host",
            "Aggregate": "/api/v1.0/repos/?user1=host1,host2&user2=host1,host2",
        }
    }
    return flask.jsonify([data])


@app.route('/api/v1.0/repos/', methods=['GET'])
def get_repos():
    ''' endpoint to fetch repos '''
    repo_data = []
    for user, hosts in flask.request.args.items():
        hosts = hosts.split(',')
        for host in hosts:
            if host == 'github':
                repo_inst = GithubRepoAPIData()
            elif host == 'bitbucket':
                repo_inst = BitbucketRepoAPIData()
            else:
                return flask.make_response(
                    flask.jsonify({'Error': 'Invalid host'}))
            result = repo_inst.query_host(user)
            if isinstance(result, list) and result[0].get("Error"):
                return flask.jsonify(
                    [{'Error': f'No user data available for {user}'}])
            repo_data.append(repo_inst.get_response())
    return flask.jsonify(GithubRepoAPIData.aggregate(repo_data))

