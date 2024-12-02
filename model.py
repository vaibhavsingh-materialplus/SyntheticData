from sdv.single_table import GaussianCopulaSynthesizer
from sdv.single_table import CTGANSynthesizer
from sdv.single_table import TVAESynthesizer
from sdv.single_table import CopulaGANSynthesizer

#from dataset import data,metadata

def GaussianCopula(data,metadata,number):
    synthesizer = GaussianCopulaSynthesizer(metadata)
#synthesizer = GaussianCopulaSynthesizer(
#    metadata, # required
#    enforce_min_max_values=True,
#    enforce_rounding=False,
#    numerical_distributions={
#        'amenities_fee': 'gaussian_kde',
#        'checkin_date': 'uniform',
#        'checkout_date': 'uniform',
#        'room_rate':'gaussian_kde'
#    },
#    default_distribution='norm'
#)
# Step 2: Train the synthesizer
    synthesizer.fit(data)
# Step 3: Generate synthetic data
    synthetic_data = synthesizer.sample(num_rows=int(f"{number}"))
    
    return synthetic_data

def CTGAN(data,metadata,number):
    synthesizer = CTGANSynthesizer(
        metadata, # required
        enforce_rounding=False,
        epochs=300,
        verbose=True,
        cuda=False)
    synthesizer.fit(data)
    synthetic_data = synthesizer.sample(num_rows=int(f"{number}"))
    return synthetic_data

def TVAE(data,metadata,number):
    synthesizer = TVAESynthesizer(
        metadata, # required
        enforce_min_max_values=True,
        enforce_rounding=False,
        epochs=300,
        cuda=False)
    
    synthesizer.fit(data)

    synthetic_data = synthesizer.sample(num_rows=int(f"{number}"))
    return synthetic_data

def CopulaGAN(data,metadata,number):
    synthesizer = CopulaGANSynthesizer(
        metadata, # required
        enforce_min_max_values=True,
        enforce_rounding=False,
    
        epochs=300,
        verbose=True,
        cuda=False)
    synthesizer.fit(data)

    synthetic_data = synthesizer.sample(num_rows=int(f"{number}"))
    return synthetic_data

