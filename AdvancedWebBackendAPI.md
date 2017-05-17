## Register [/register] [POST]

+ Request 

{
    id : (char max 100)
    password : (char max 100)
    name : (char max 100)
    role : ('STUDENT' or 'TEACHER')
}

+ Response 201

created

{}

+ Response 409

id confliction

{}

+ Response 400

other kind of error

{}

## Login [/login] [POST]

+ Request

{
    id
    password
} 

+ Response 200

{
    id
    name
    role
}

+ Response 400

failure

{}

## Logout [/logout] [DELETE]

+ Request

{}

+ Response 200

{}

## Tree [/tree]

### Get Tree [GET]

+ Request

{}

+ Response 200

{ tree data }

+ Response 403

{}

+ Response 404
no tree

### Set Tree [POST]

+ Request

{ tree data }

+ Response 200

{}

+ Response 403

{}

## Set Homework [/node/<node_id>/homework] [POST]

+ Request

{
    published : (true or false)
    questions:[
        {
           type : ('CHOICE' or 'TEXT')
           question : (char max 100)
           A : (char max 100)
           B : (char max 100)
           C : (char max 100)
           D : (char max 100)
           correct_answer : (char max 100) 
        }
        ...
    ]
}

example

{
	"questions": [
		{
			"type": "TEXT",
			"question": "what the fuck",
			"A": null,
			"B": null,
			"C": null,
			"D": null,
			"correct_answer": null,
			"order": 0
		},
		{
			"type": "CHOICE",
			"question": "who the fuck",
			"A": "a",
			"B": "b",
			"C": "c",
			"D": "d",
			"correct_answer": "abc",
			"order": 0
		}
	],
	"published": false,
	"node_id": 10
}


+ Response 403

{}


## Get Homework [/node/<node_id>/homework] [GET]

+ Request
{}

+ Response 200

{
	"questions": [
		{
			"id": 5,
			"type": "TEXT",
			"question": "what the fuck",
			"A": null,
			"B": null,
			"C": null,
			"D": null,
			"correct_answer": null,
			"order": 0
		},
		{
			"id": 6,
			"type": "CHOICE",
			"question": "who the fuck",
			"A": "a",
			"B": "b",
			"C": "c",
			"D": "d",
			"correct_answer": "abc",
			"order": 1
		}
	],
	"published": false,
	"node_id": 10
}

+ Response 403

{}

+ Response 404

{}

## Get Homework Answer of a student [/node/<node_id>/homework_answer] [GET]

+ Request

{}

+ Response 200

{
    "answers":[
        {
            "answer" : (answer text)
            "question" : (id of corresponding question)
        }
        ...
    ]
}

example

{
	"answers": [
		{
			"answer": "jalksdkjfioasdjhgpiowjrsopfgkj;pswjhb;p'ir5wnjmhp",
			"question": 5
		},
		{
			"answer": "l;sdkjfgkswjdiogw2pirjgkpowrkhgp-oeswrnjmhboieswjrghpijwrf",
			"question": 4
		}
	],
}

+ Response 403

{}

+ Response 404

{}

## Set homework answer for a student [/node/<node_id>/homework_answer] [POST]

+ Request

{
	"answers": [
		{
			"answer": "aaaaaaaaaaaaa",
			"question": 5
		},
		{
			"answer": "ccccccccccccccc",
			"question": 4
		}
	]
}

+ Response 200

{}

+ Response 400

something wrong with the request data

{}

+ Response 404

no corresponding homework

{}

+ Response 403

{}

## Get Material List of a Node [/node/<node_id>/materials] [GET]

+ Request

{}

+ Response 200

{
	"materials": [
		{
			"id": 1,
			"material_file": "materials/4c68b62e-d25f-48bb-b811-011744cea1baScreenshot_from_2017-04-27_03-41-13..png"
		},
		{
			"id": 2,
			"material_file": "materials/acd37ddc-35a0-4c0d-9186-3276c93d282bScreenshot_from_2017-04-28_20-50-31..png"
		},
		{
			"id": 3,
			"material_file": "materials/df19e32f-bd80-42db-9e09-5b38f9ba925cScreenshot_from_2017-05-11_19-53-59..png"
		}
	],
	"id": 1
}

+ Response 403

{}

+ Response 404

{}

## Upload Material [/node/<node_id>/material] [POST]

+ Request

post the file

{}

+ Response 201

{}

+ Response 400

no file attached

{}

+ Response 403

{}

## Download Material [/node/<node_id>/material/<material_id>] [GET]

+ Request

{}

+ Response 200

download file as attachment

{}

+ Response 403

{}

+ Response 404

no corresponding material
 
{}