# app.py (main file)

from flask import request, jsonify, make_response, json
from sqlalchemy.exc import OperationalError
from werkzeug.exceptions import HTTPException

from src.init_app import app, db
from src.models import VoteCount, VoteCountSchema

# Create instance of schemas
voteCountSchema = VoteCountSchema(many = False)


"""
    The function handle_exception() return error response in json format
        response = {
            "status code" : status code of the error,
            "error" : name of the error,
            "description" : description of the error
        }
"""

# HTTP Error handndler
@app.errorhandler(HTTPException)

# This function will handle error from HTTPException
def handle_exception(e):

    # Get the response from the error
    response = e.get_response()

    # Get the status code, name, description from the error
    response.data = json.dumps({
        "status code" : e.code,
        "error" : e.name,
        "description" : e.description
    })

    # Define the request body format is JSON.
    response.content_type = "application/json"

    return response

# OperationalError handler
@app.errorhandler(OperationalError)

# This function will handle error from OperationalError
def handle_exception(e):

    return make_response(jsonify({
            "status code" : "None",
            "error" : "Database connection error",
            "description" : "{}".format(str(e))
        }))

#create route for add vote to candidate (api/vote)
@app.route('/api/vote', methods = ['POST'])

def add_vote():
    """
    This function will accept POST request with a body
    with type JSON
        body : 
            {"candidate" : <string>}
    """
    try:
        candidate = request.json['candidate']
        votes = 1

        # Check whether the given candidate name is exist in the table or not
        ex_candidate = VoteCount.query \
        .filter(VoteCount.candidate == candidate) \
        .one_or_none()

        # if given candidate name is not in the table
        if ex_candidate is None:

            # create a new candidate
            ex_candidate = VoteCount(candidate = candidate, votes = votes)
            
            # add the new candidate to the table
            db.session.add(ex_candidate)
            db.session.commit()
            
        # if the given candidate is exist in the table
        else:

            # update existing candidate vote count
            ex_candidate.votes += 1
            db.session.commit()

        # return the candidate details in json format
        return voteCountSchema.jsonify(ex_candidate)

    # Check for KeyError 
    except KeyError:
        return make_response(jsonify({
            "status code" : "None",
            "error" : "KeyError",
            "description" : "The given keyword was not found. Please check and try again."
        }))

# get candidate vote count (api/candidate/<int:candidate_id>/count)
@app.route('/api/candidate/<int:candidate_id>/count', methods = ['GET'])

# Get the candidate deails with the given candidate_id 
def get_vote_count(candidate_id):

    # Get the details of the candidate with the given candidate_id
    candidate = VoteCount.query \
    .filter(VoteCount.id == candidate_id) \
    .one_or_none()

    # if the candidate with the candidate_id is exist
    if candidate is not None:

        # Serialize the data for the response
        data = voteCountSchema.dump(candidate)

        # Log the vote count to console
        app.logger.info(candidate.votes)

        # return the vote count
        return {"votes" : candidate.votes}

    # if the candidate with candidate_id is not exist
    else:
        # return error response Not found error
        return make_response(jsonify({
        "status code" : "404",
        "error" : "Not Found",
        "description" : "Candidate not found for Id: {candidate_id}"
        }))

# main function
if __name__ == '__main__':
    app.debug = True
    app.run()

