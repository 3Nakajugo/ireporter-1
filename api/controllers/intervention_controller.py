from flask import jsonify, request
from api.models.incident import Incident
from api.utility.validation import ValidateRecord
from api.database.db import DatabaseConnection
from datetime import datetime
from api.authentication.auth import get_current_identity, extract_token_from_header, token_required

db_conn = DatabaseConnection()


class InterventionController():
    def __init__(self):
        pass

    def create_intervention_record(self):
        data = request.get_json()

        created_by = data.get("createdBy")
        incident_type = data.get("type")
        status = data.get("incident_status")
        images = data.get("Images")
        location = data.get("incident_location")
        videos = data.get("Videos")
        comments = data.get("comment")

        # if not created_by or not created_on or not incident_type or not location \
        #         or not status or not images \
        #         or not videos or not comments:
        #     return jsonify({
        #         "Message": "Insert required fields"
        #     }), 400

        # if not ValidateRecord.validate_type(incident_type):
        #     return jsonify({'status': 400,
        #                     'Error': 'type must a string and must be a red-flag'
        #                     }), 400
        # if not ValidateRecord.validate_comment(comments):
        #     return jsonify({'status': 400,
        #                     'error': 'comment must be a string'}), 400

        # if not ValidateRecord.validate_status(status):
        #     return jsonify({'status': 400,
        #                     'error': "Status must either be resolved, rejected or under investigation"
        #                     }), 400
        # if not ValidateRecord.validate_location(red_flag_location):
        #     return jsonify({'status': 400,
        #                     'error': 'Location field only takes in a list of valid Lat and Long cordinates'
        #                     }), 400

        intervention = Incident(createdBy=created_by, type=incident_type,
                                incident_location=location, incident_status=status,
                                Images=images, Videos=videos, comment=comments)

        db_conn.insert_incident(
            created_by, incident_type, status, images, location, videos, comments)
        return jsonify({
            "status": 201,
            "Message": "Created record"
        }), 201

    def get_all_intervention_records(self):
        if len(my_red_flags) > 0:
            return jsonify({
                "status": 200,
                "data": [red_flag for red_flag in my_red_flags]
            }), 200
        return jsonify({
            "status": 400,
            "Error": "There are no records"
        })

    def get_an_intervention_record(self, flag_id):
        red_flag_record = [
            red_flag for red_flag in my_red_flags if red_flag['id'] == flag_id]
        if red_flag_record:
            return jsonify({
                "status": 200,
                "redflag": red_flag_record
            }), 200
        return jsonify({
            "status": 404,
            "Error": " Record does not exist"
        }), 404

    def delete_red_flag(self, flag_id):
        red_flag_record = [
            flag for flag in my_red_flags if flag['id'] == flag_id]
        if len(my_red_flags) == 0:
            return jsonify({
                "status": "200",
                "Error": "There is nothing found"
            }), 200
        my_red_flags.remove(red_flag_record[0])
        return jsonify({
            'Result': "record was deleted successfully"
        }), 200

    def edit_intervention_location(self, flag_id):
        data = request.get_json()
        for red_flag_record in my_red_flags:
            if red_flag_record['id'] == flag_id:
                red_flag_record["location"] = data["location"]
                return jsonify({
                    "data": red_flag_record,
                    "status": 200,
                    "message": "Updated red-flag's record location"
                }), 200
            if not red_flag_record:
                return jsonify({
                    "status": "400",
                    "Error": "Red flag is not available"
                }), 400

    def edit_intervention_comment(self, flag_id):
        data = request.get_json()
        for red_flag_record in my_red_flags:
            if red_flag_record['id'] == flag_id:
                red_flag_record["comment"] = data["comment"]
                return jsonify({
                    "data": red_flag_record,
                    "status": 200,
                    "message": "Updated red-flag's record comment"
                }), 200
            if not red_flag_record:
                return jsonify({
                    "status": "400",
                    "Error": "Red flag is not available"
                })
