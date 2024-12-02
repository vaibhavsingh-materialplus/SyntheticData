from sdv.datasets.demo import get_available_demos
from sdv.datasets.demo import download_demo


print(get_available_demos(modality='single_table'))

def dataset_download(name):
    data, metadata = download_demo(
        modality='single_table',
        dataset_name=f"{name}"
    )
    data.to_csv(f'{name}.csv', index=False)
    return data,metadata
    
