# python-practice (grouping set)

## This repo contains simple coding excercise for the following questions: 

Please do same exercise using two different framework.

Framework 1. panda

Framework 2. apache beam python https://beam.apache.org/documentation/sdks/python/

Framework 3. pyspark


using two input files dataset1 and dataset2

join dataset1 with dataset2 and get tier

generate below output file:

legal_entity, counterparty, tier, max(rating by counterparty), sum(value where status=ARAP), 
sum(value where status=ACCR)

Also create new record to add total for each of legal entity, counterparty & tier.

Sample data:

legal_entity, counterparty, tier,   max(rating by counterparty), sum(value where status=ARAP), sum(value where status=ACCR)
   
    L1,         Total,      Total,  calculated_value,            calculated_value,             calculated_value
    L1,         C1,         Total,  calculated_value,            calculated_value,             calculated_value
    Total,      C1,         Total,  calculated_value,            calculated_value,             calculated_value
    Total,      Total,      1,      calculated_value,            calculated_value,             calculated_value
    L2,         Total,      Total,  calculated_value,            calculated_value,             calculated_value
....
like all other values.

where caluclated_value in sample data needs to be calculated using above method.
