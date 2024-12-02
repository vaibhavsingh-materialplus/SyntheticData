from model import synthetic_data

# save the data as a CSV
synthetic_data.to_csv('synthetic_data.csv', index=False)