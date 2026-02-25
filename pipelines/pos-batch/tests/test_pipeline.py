import apache_beam as beam
import pytest
from pipeline import ParsePosTransaction

def test_parse_pos_transaction():
    test_line = "TX123,STORE001,PROD456,25.99,2026-02-23"
    runner = beam.runners.interactive.interactive_runner.InteractiveRunner()
    
    with beam.Pipeline(runner=runner) as p:
        result = (p 
                 | beam.Create([test_line])
                 | beam.ParDo(ParsePosTransaction())
                 | beam.Map(print))
    
    assert result.result == 1  # Should process 1 record
