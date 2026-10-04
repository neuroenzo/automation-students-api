STUDENT = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer",
        },
        "name": {
            "type": "string",
        },
        "email": {
            "type": "string",
        },
        "phone_no": {
            "type": "string",
        },
        "gender": {
            "type": "string",
            "enum": ["male", "female"],
        },
        "status": {
            "type": "integer",
            "enum": [0, 1],
        },
    },
    "required": [
        "id",
        "name",
        "email",
        "phone_no",
        "gender",
        "status",
    ],
}


STUDENTS = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "status": {
            "type": "integer",
            "enum": [0, 1],
        },
        "students": {
            "type": "array",
            "items": STUDENT,
        },
    },
    "required": [
        "status",
        "students",
    ],
}


CREATE_STUDENT_RESPONSE = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "message": {
            "type": "string",
        },
        "status": {
            "type": "integer",
            "enum": [0, 1],
        },
        "student": STUDENT,
    },
    "required": [
        "message",
        "status",
        "student",
    ],
}
