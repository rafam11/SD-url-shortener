#!/bin/bash
set -e

ROOT_USER="${MONGO_INITDB_ROOT_USERNAME}"
ROOT_PASSWORD="${MONGO_INITDB_ROOT_PASSWORD}"
DB_NAME="${MONGO_INITDB_DATABASE}"

mongosh -u "$ROOT_USER" -p "$ROOT_PASSWORD" --authenticationDatabase admin <<EOF

use $DB_NAME;

db.createUser(
    {
        user: "$ROOT_USER",
        pwd: "$ROOT_PASSWORD",
        roles: [
            {
                role: "readWrite",
                db: "$DB_NAME"
            }
        ]
    }
);

if (db.getCollectionNames().includes("urls")) {
    print("Collection 'urls' already exists.")
} else {
    db.createCollection("urls", {
        validator: {
            \$jsonSchema: {
                bsonType: "object",
                title: "URL object validation",
                required: [
                    "_id",
                    "short_url",
                    "long_url",
                    "created_at",
                    "expires_at",
                    "user_id",
                    "is_active",
                    "click_count"
                ],
                properties: {
                    _id: {
                        bsonType: "objectId",
                        description: "MongoDB unique identifier for the document"
                    },
                    short_url: {
                        bsonType: "string",
                        description: "'short_url' must be a string and is required"
                    },
                    long_url: {
                        bsonType: "string",
                        description: "'long_url' must be a string and is required"
                    },
                    created_at: {
                        bsonType: "date",
                        description: "'created_at' must be a date and is required"
                    },
                    expires_at: {
                        bsonType: "date",
                        description: "'expires_at' must be a date and is required"
                    },
                    user_id: {
                        bsonType: "long",
                        description: "'user_id' must be a long and is required"
                    },
                    is_active: {
                        bsonType: "bool",
                        description: "'is_active' must be a bool and is required"
                    },
                    last_accessed_at: {
                        bsonType: ["date", "null"],
                        description: "'last_accessed_at' must be a date"
                    },
                    click_count: {
                        bsonType: "int",
                        description: "'click_count' must be an int and is required"
                    },
                },
                additionalProperties: false
            }
        }
    })

    db.urls.createIndex(
        {
            short_url: 1
        },
        {
            unique: true
        }
    )
};
EOF

echo "MongoDB initialized"
