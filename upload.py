from sdv.datasets.local import load_csvs
from sdv.metadata import Metadata



def process_csv():
    # assume that my_folder contains a CSV file named 'guests.csv'
    datasets = load_csvs(
        folder_name='./my_folder',
        read_csv_parameters={
            'skipinitialspace': True,
            'encoding': 'utf_8'
        })
    print(datasets)
    first_key = list(datasets.keys())[0]
    # the data is available under the file name
    print(type(datasets[first_key]))
    #data = datasets['guests']


    metadata = Metadata.detect_from_dataframe(
        data=datasets[first_key],
        table_name='my_data')

    print(type(metadata))
    print(metadata)
    
    return datasets[first_key], metadata
