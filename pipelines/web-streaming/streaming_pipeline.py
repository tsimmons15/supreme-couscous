import apache_beam as beam
import argparse
import json
import logging
from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions
from apache_beam.io.gcp.bigquery import BigQueryDisposition

class ParseWebEvent(beam.DoFn):
    def process(self, element):
        try:
            data, _ = element
            event = json.loads(data.decode('utf-8'))
            
            yield {
                'event_id': event.get('event_id'),
                'user_id': event.get('user_id', 'anonymous'),
                'session_id': event.get('session_id'),
                'event_type': event.get('event_type'),
                'product_id': event.get('product_id'),
                'timestamp': event.get('timestamp'),
                'event_date': event.get('timestamp', '')[:10]
            }
        except Exception as e:
            logging.error(f"Parse error: {e}")

def run_pipeline(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_topic', required=True)
    parser.add_argument('--output_table', required=True)
    known_args, pipeline_args = parser.parse_known_args(argv)
    
    pipeline_options = PipelineOptions(pipeline_args)
    google_cloud_options = pipeline_options.view_as(GoogleCloudOptions)
    google_cloud_options.streaming = True
    google_cloud_options.region = 'us-east1'
    
    schema = {
        'fields': [
            {'name': 'event_id', 'type': 'STRING'},
            {'name': 'user_id', 'type': 'STRING'},
            {'name': 'session_id', 'type': 'STRING'},
            {'name': 'event_type', 'type': 'STRING'},
            {'name': 'product_id', 'type': 'STRING'},
            {'name': 'timestamp', 'type': 'TIMESTAMP'},
            {'name': 'event_date', 'type': 'DATE'}
        ]
    }
    
    with beam.Pipeline(options=pipeline_options) as p:
        (p 
         | 'Read PubSub' >> beam.io.ReadFromPubSub(topic=known_args.input_topic)
         | 'Parse Events' >> beam.ParDo(ParseWebEvent())
         | 'Window Hours' >> beam.WindowInto(beam.window.FixedWindows(3600))
         | 'Write BQ' >> beam.io.WriteToBigQuery(
             known_args.output_table,
             schema=schema,
             create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
             write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
             time_partitioning=beam.io.gcp.bigquery.TimePartitioning(
                 type_=beam.io.gcp.bigquery.TimePartitioning.Type.DAY,
                 field='event_date'
             ),
             clustering_fields=['session_id', 'user_id']
         ))

if __name__ == '__main__':
    run_pipeline()
