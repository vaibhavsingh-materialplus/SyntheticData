from sdv.evaluation.single_table import run_diagnostic, evaluate_quality
#from sdv.evaluation.single_table import get_column_plot, get_column_pair_plot
#from main import synthetic_data
#from dataset import data, metadata

def metrics(data,metadata,synthetic_data):
# 1. perform basic validity checks
    diagnostic = run_diagnostic(data, synthetic_data, metadata)

# 2. measure the statistical similarity
    quality_report = evaluate_quality(data, synthetic_data, metadata)
    print(type(quality_report))
    print(type(diagnostic))
    print(type(quality_report.get_details(property_name='Column Shapes')))
# 3. plot the data
    #fig = get_column_plot(
     #   real_data=data,
      #  synthetic_data=synthetic_data,
      #  metadata=metadata,
      #  column_name='amenities_fee'
    #)
    
#fig.show()
    print(diagnostic)
    print("/n")
    print(quality_report)
    print("/n")
    print(quality_report.get_details(property_name='Column Shapes'))
    column_quality_report=quality_report.get_details(property_name='Column Shapes')
    column_pair_trends=quality_report.get_details(property_name='Column Pair Trends')
    data_validity=diagnostic.get_details(property_name='Data Validity')
    data_structure=diagnostic.get_details(property_name='Data Structure')
    return column_quality_report,column_pair_trends,data_validity,data_structure
