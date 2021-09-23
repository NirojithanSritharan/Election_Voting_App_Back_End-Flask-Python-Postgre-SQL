from flask import request, jsonify, make_response, json, abort
from sqlalchemy.exc import OperationalError
from werkzeug.exceptions import HTTPException

from src.init_app import app, db
from src.models import VoteCount, VoteCountSchema

# create instance of schemas
voteCountSchemas = VoteCountSchema(many = True)
voteCountSchema = VoteCountSchema(many = False)

@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()

    response.data = json.dumps({
        "status code" : e.code,
        "error" : e.name,
        "description" : e.description
    })

    response.content_type = "application/json"

    return response

@app.errorhandler(OperationalError)
def handle_exception(e):

    return make_response(jsonify({
            "status code" : "None",
            "error" : "Database connection error",
            "description" : "{}".format(str(e))
        }))

#create routes for new candidate
@app.route('/api/vote', methods = ['POST'])
def add_vote():

    try:
        candidate = request.json['candidate']
        votes = 1

        ex_candidate = VoteCount.query \
        .filter(VoteCount.candidate == candidate) \
        .one_or_none()

        if ex_candidate is None:
            # create a new candidate
            ex_candidate = VoteCount(candidate = candidate, votes = votes)
            db.session.add(ex_candidate)
            
        else:
            # update existing candidate vote
            ex_candidate.votes += 1
            db.session.commit()

        return voteCountSchema.jsonify(ex_candidate)

    except KeyError:
        return make_response(jsonify({
            "status code" : "None",
            "error" : "KeyError",
            "description" : "The given keyword was not found. Please check and try again."
        }))

    # except sqlalchemy.exc.OperationalError as exc:
    #     logging.exception("METRICS: error while gathering metrics")
    #     stats = {
    #         "health": {
    #         "health": 0,
    #         "diagnosis": "Database error: {}".format(str(exc)),
    #             }
    #         }
    #     return stats 
    # except Exception as e:
    #     response = e.get_response()

    #     response.data = json.dumps({
    #         "code" : e.code,
    #         "name" : e.name,
    #         "description" : e.description
    #     })

    #     response.content_type = "application/json"

        # return str(e)

# get candidate vote count
@app.route('/api/candidate/<int:candidate_id>/count', methods = ['GET'])

# Get the candidate deails with the given candidate_id 
def get_vote_count(candidate_id):

    # try:
        # candidate = VoteCount.query.get_or_404(int(candidate_id))
        
        candidate = VoteCount.query \
        .filter(VoteCount.id == candidate_id) \
        .one_or_none()

        # Did we find a person?
        if candidate is not None:

            # Serialize the data for the response
            data = voteCountSchema.dump(candidate)

            app.logger.info(candidate.votes)

            return {"votes" : candidate.votes}

        else:
            return make_response(jsonify({
            "status code" : "404",
            "error" : "Not Found",
            "description" : "Candidate not found for Id: {candidate_id}"
        }))

    # except Exception as e:
    #     print(e)
    #     return {"error" : str(e)}

if __name__ == '__main__':
    app.debug = True
    app.run()

