import apache_beam as beam
import argparse
import logging
from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions
from apache_beam.io.gcp.bigquery import BigQueryDisposition

class ParsePosTransaction(beam.DoFn):
    def process(self, element):
        try:
            if element.startswith('transaction_id'): return
            fields = element.strip().split(',')
            if len(fields) < 5: return
                
            yield {
                'transaction_id': fields[0].strip(),
                'store_id': fields[1].strip(),
                'product_id': fields[2].strip(),
                'amount': float(fields[3]),
                'transaction_date': fields[4].strip()
            }
        except Exception as e:
            logging.error(f"Parse error: {e}")

def run_pipeline(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    known_args, pipeline_args = parser.parse_known_args(argv)
    
    pipeline_options = PipelineOptions(pipeline_args)
    google_cloud_options = pipeline_options.view_as(GoogleCloudOptions)
    google_cloud_options.region = 'us-east1'
    
    schema = {
        'fields': [
            {'name': 'transaction_id', 'type': 'STRING'},
            {'name': 'store_id', 'type': 'STRING'},
            {'name': 'product_id', 'type': 'STRING'},
            {'name': 'amount', 'type': 'FLOAT'},
            {'name': 'transaction_date', 'type': 'DATE'}
        ]
    }
    
    with beam.Pipeline(options=pipeline_options) as p:
        (p 
         | 'Read CSV' >> beam.io.ReadFromText(known_args.input, skip_header_lines=1)
         | 'Parse POS' >> beam.ParDo(ParsePosTransaction())
         | 'Write BQ' >> beam.io.WriteToBigQuery(
             known_args.output,
             schema=schema,
             create_disposition=BigQueryDisposition.CREATE_IF_NEEDED,
             write_disposition=BigQueryDisposition.WRITE_TRUNCATE,
             time_partitioning=beam.io.gcp.bigquery.TimePartitioning(
                 type_=beam.io.gcp.bigquery.TimePartitioning.Type.DAY,
                 field='transaction_date'
             ),
             clustering_fields=['store_id', 'product_id']
         ))

if __name__ == '__main__':
    run_pipeline()
