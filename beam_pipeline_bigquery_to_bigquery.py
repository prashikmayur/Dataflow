import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, SetupOptions, StandardOptions

class BigQueryToBigQueryOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument('--source_table', required=True, help='BigQuery Source Table')
        parser.add_argument('--destination_table', required=True, help='BigQuery Destination Table')

def run():
    # Parse pipeline options
    options = BigQueryToBigQueryOptions()
    standard_options = options.view_as(StandardOptions)
    standard_options.runner = 'DataflowRunner'

    # Log all options for debugging
    print("Pipeline Options:")
    for key, value in options.get_all_options().items():
        print(f"{key}: {value}")

    with beam.Pipeline(options=options) as pipeline:
        (
            pipeline
            | 'Read from BigQuery' >> beam.io.ReadFromBigQuery(
                query=f"SELECT * FROM `{options.source_table}`",
                use_standard_sql=True
            )
            | 'Write to BigQuery' >> beam.io.WriteToBigQuery(
                options.destination_table,
                write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
            )
        )

if __name__ == '__main__':
    run()
