db = db.getSiblingDB('cmlredb');

db.createCollection('ecomorphology_records', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['species_id', 'collection_date'],
      properties: {
        species_id: { bsonType: 'string' },
        worms_id: { bsonType: 'int' },
        collection_date: { bsonType: 'date' },
        body_length_mm: { bsonType: 'double' },
        body_weight_g: { bsonType: 'double' },
        habitat_guild: { bsonType: 'string' },
        morphometric_measurements: { bsonType: 'object' },
        annotations: { bsonType: 'array' }
      }
    }
  }
});

db.createCollection('pipeline_jobs', {});
db.createCollection('bert_index_metadata', {});

db.ecomorphology_records.createIndex({ species_id: 1 });
db.ecomorphology_records.createIndex({ collection_date: -1 });
db.pipeline_jobs.createIndex({ job_id: 1 }, { unique: true });
db.pipeline_jobs.createIndex({ status: 1, created_at: -1 });
