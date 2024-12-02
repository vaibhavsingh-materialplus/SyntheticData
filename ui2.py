import gradio as gr
import pandas as pd
from dataset import dataset_download
from model import GaussianCopula, CTGAN, TVAE, CopulaGAN
from evaluation import metrics
#from sdv.evaluation.single_table import get_column_plot,get_column_pair_plot
#from visualize import get_column_plot,get_column_pair_plot
from single_table import get_column_pair_plot,get_column_plot,get_column_triple_plot
import shutil,os
from upload import process_csv
# Define the folder to save uploaded CSV files
SAVE_FOLDER = "my_folder"

# Create the folder if it doesn't exist
os.makedirs(SAVE_FOLDER, exist_ok=True)

def delete_all_files_in_folder(folder_path='my_folder'):
    # Check if the folder exists
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        # Iterate over all files and directories in the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            # Check if it is a file and delete it
            if os.path.isfile(file_path):
                os.remove(file_path)
            # Check if it is a directory and delete it
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        print("All files in the folder have been deleted.")
    else:
        print("The folder does not exist or is not a directory.")


def save_csv_in_a_folder(file):
    file_path = os.path.join(SAVE_FOLDER, file.split('/')[-1])
    shutil.copy(file, file_path)


class Dataset:
    def initialize(self, data, metadata, synthetic_data):
        self.real_data = data
        self.metadata = metadata
        self.synthetic_data = synthetic_data

# Define dataset_instance as a global variable
dataset_instance = Dataset()

# Function to create a Plotly graph
def plot_from_text(column,dataset_instance):
    #fig = px.scatter(df, x=df.columns[0], y=df.columns[1], title="Synthetic Data Scatter Plot")
    fig = get_column_plot(
        real_data=dataset_instance.real_data,
        synthetic_data=None,
        metadata=dataset_instance.metadata,
        column_name=f"{column}"
        )
    return fig


# Function to create a Plotly graph
def plot_from_text1(column1,column2,column3,dataset_instance):
    #fig = px.scatter(df, x=df.columns[0], y=df.columns[1], title="Synthetic Data Scatter Plot")
    fig = get_column_pair_plot(
        real_data=dataset_instance.real_data,
        synthetic_data=None,
        metadata=dataset_instance.metadata,
        column_names=[f"{column1}",f"{column2}",f"{column3}"]
        )
    return fig


def plot_from_text2(column1,column2,column3,dataset_instance):
    #fig = px.scatter(df, x=df.columns[0], y=df.columns[1], title="Synthetic Data Scatter Plot")
    fig = get_column_triple_plot(
        real_data=dataset_instance.real_data,
        synthetic_data=None,
        metadata=dataset_instance.metadata,
        column_names=[f"{column1}",f"{column2}",f"{column3}"]
        )
    return fig

def process_selection2(selection1, selection2,number):
    global dataset_instance  # Ensure we are modifying the global dataset_instance
    data, metadata = dataset_download(selection2)

    # Generate synthetic data based on model selection
    if selection1 == "Gaussian Copula":
        synthetic_data = GaussianCopula(data, metadata,number)
    elif selection1 == "CTGAN":
        synthetic_data = CTGAN(data, metadata,number)
    elif selection1 == "TVAE":
        synthetic_data = TVAE(data, metadata,number)
    elif selection1 == "CopulaGAN":
        synthetic_data = CopulaGAN(data, metadata,number)

    # Convert to DataFrame and save as CSV
    df = pd.DataFrame(synthetic_data)
    dataset_instance.initialize(data, metadata, synthetic_data)
    
    csv_file = "./result.csv"
    df.to_csv(csv_file, index=False)
    
    # Generate report summary
    column_quality_report,column_pair_trends,data_validity,data_structure = metrics(data,metadata,synthetic_data)
    
    # Return both CSV file path and report summary
    return csv_file, column_quality_report,column_pair_trends,data_validity,data_structure,data.head(),df.head(),data.shape,df.shape


def process_selection1(selection1,number):
    global dataset_instance  # Ensure we are modifying the global dataset_instance
    #data, metadata = dataset_download(selection2)
    data,metadata=process_csv()
    # Generate synthetic data based on model selection
    if selection1 == "Gaussian Copula":
        synthetic_data = GaussianCopula(data, metadata,number)
    elif selection1 == "CTGAN":
        synthetic_data = CTGAN(data, metadata, number)
    elif selection1 == "TVAE":
        synthetic_data = TVAE(data, metadata, number)
    elif selection1 == "CopulaGAN":
        synthetic_data = CopulaGAN(data, metadata, number)

    # Convert to DataFrame and save as CSV
    df = pd.DataFrame(synthetic_data)
    dataset_instance.initialize(data, metadata, synthetic_data)
    
    csv_file = "./result.csv"
    df.to_csv(csv_file, index=False)
    
    # Generate report summary
    column_quality_report,column_pair_trends,data_validity,data_structure = metrics(data,metadata,synthetic_data)
    #shutil.rmtree("./my_folder")

    # Return both CSV file path and report summary
    return csv_file, column_quality_report,column_pair_trends,data_validity,data_structure,data.head(),df.head(),data.shape,df.shape

# Create the Gradio Interface with 3 tabs
with gr.Blocks() as demo:
    with gr.Tab("Generate Synthetic Data from your own Dataset"):
        with gr.Row():
            with gr.Row():
                
                file_input = gr.File(label="Upload your CSV file")
                submit_btn = gr.Button("Upload")
            submit_btn.click(save_csv_in_a_folder, inputs=file_input)
            # Dropdown options
            dropdown_options_in_first_tab = ["Gaussian Copula", "CTGAN", "TVAE", "CopulaGAN"]
            #dropdown_options2 = ["insurance", "fake_companies", "child", "census_extended", "census", "asia", "KRK_v1", "adult", "alarm", "covtype", "credit", "expedia_hotel_logs", "fake_hotel_guests", "grid", "gridr", "intrusion", "mnist12", "news", "ring", "student_placements", "student_placements_pii"]
            number_input1 = gr.Textbox(label="Input Number of rows you want to synthesize:")
            dropdown_options_for_first_tab = gr.Dropdown(label="Select Model", choices=dropdown_options_in_first_tab)
            #dropdown2 = gr.Dropdown(label="Select Dataset", choices=dropdown_options2)
            
        with gr.Row():
            
            real_data_row_column1=gr.Textbox(label="Rows and columns in Real Data",interactive=False)
            synthetic_data_row_column1=gr.Textbox(label="Rows and columns in Synthetic Data", interactive=False)
            output_csv1 = gr.File(label="Download CSV")
    
    
        # DataFrame display element
        with gr.Row():
            df_display11 = gr.DataFrame(label="Real Data Preview", interactive=False)
            df_display12 = gr.DataFrame(label="Synthetic Data Preview", interactive=False)
        
        # Pre-recorded information for the table
        gr.Markdown("### About the Methods to synthesize data:")
        pre_recorded_data = {
                "Method": ["GaussianCopula", "CTGAN (Conditional Tabular GAN)","TVAE (Tabular Variational Autoencoder)","CopulaGAN"],
                "Best For": ["Smaller, simpler datasets with mostly Gaussian distributions.", "Tabular data with imbalanced categories or rare feature combinations","High-dimensional datasets where complex feature interactions need to be captured.","Tabular data where feature relationships are critical, especially those with specific dependencies."],
                "Advantages":["- Fast and lightweight- Performs well on low-dimensional data and simple relationships","- Excels at generating realistic categorical and non-Gaussian data- Handles class imbalance effectively","- Can handle complex relationships and high-dimensional data- Better for non-Gaussian distributions","- Good for reproducing complex statistical dependencies- Balances GAN’s realism with copula dependency modeling"],
                "Limitations":["- Limited to Gaussian-like data distributions- Struggles with highly skewed or complex non-linear relationships","- Computationally intensive- Requires a large amount of data to train effectively","- Longer training time- May require more hyperparameter tuning than simpler models","- Less flexible with high-dimensional data- More complex to configure for custom dependencies"]
                }
        pre_recorded_df = pd.DataFrame(pre_recorded_data)
        # DataFrame display element for pre-recorded data
        pre_recorded_display = gr.DataFrame(value=pre_recorded_df, interactive=False)
        
        delete_datasets_button = gr.Button("Delete Uploaded Datasets")
        
        delete_datasets_button.click(delete_all_files_in_folder)
    with gr.Tab("Generate Synthetic Data from available Datasets"):
        with gr.Row():
            # Dropdown options
            dropdown_options1 = ["Gaussian Copula", "CTGAN", "TVAE", "CopulaGAN"]
            dropdown_options2 = ["insurance", "fake_companies", "child", "census_extended", "census", "asia", "KRK_v1", "adult", "alarm", "covtype", "credit", "expedia_hotel_logs", "fake_hotel_guests", "grid", "gridr", "intrusion", "mnist12", "news", "ring", "student_placements", "student_placements_pii"]

            dropdown1 = gr.Dropdown(label="Select Model", choices=dropdown_options1)
            number_input2 = gr.Textbox(label="Input Number of rows you want to synthesize:")
            dropdown2 = gr.Dropdown(label="Select Dataset", choices=dropdown_options2)
            
        with gr.Row():
            real_data_row_column2=gr.Textbox(label="Rows and columns in Real Data",interactive=False)
            synthetic_data_row_column2=gr.Textbox(label="Rows and columns in Synthetic Data", interactive=False)
            output_csv2 = gr.File(label="Download CSV")

    
    
        # DataFrame display element
        with gr.Row():
            df_display21 = gr.DataFrame(label="Real Data Preview", interactive=False)
            df_display22 = gr.DataFrame(label="Synthetic Data Preview", interactive=False)
        
        
        # Pre-recorded information for the table
        gr.Markdown("### About the Methods to synthesize data:")
        pre_recorded_data = {
                "Method": ["GaussianCopula", "CTGAN (Conditional Tabular GAN)","TVAE (Tabular Variational Autoencoder)","CopulaGAN"],
                "Best For": ["Smaller, simpler datasets with mostly Gaussian distributions.", "Tabular data with imbalanced categories or rare feature combinations","High-dimensional datasets where complex feature interactions need to be captured.","Tabular data where feature relationships are critical, especially those with specific dependencies."],
                "Advantages":["- Fast and lightweight- Performs well on low-dimensional data and simple relationships","- Excels at generating realistic categorical and non-Gaussian data- Handles class imbalance effectively","- Can handle complex relationships and high-dimensional data- Better for non-Gaussian distributions","- Good for reproducing complex statistical dependencies- Balances GAN’s realism with copula dependency modeling"],
                "Limitations":["- Limited to Gaussian-like data distributions- Struggles with highly skewed or complex non-linear relationships","- Computationally intensive- Requires a large amount of data to train effectively","- Longer training time- May require more hyperparameter tuning than simpler models","- Less flexible with high-dimensional data- More complex to configure for custom dependencies"]
                }
        pre_recorded_df = pd.DataFrame(pre_recorded_data)
        # DataFrame display element for pre-recorded data
        pre_recorded_display = gr.DataFrame(value=pre_recorded_df, interactive=False)
        
    
    with gr.Tab("Evaluate Synthetic Data"):
        
        gr.Markdown(r"""
                -> The statistical similarity between the real and synthetic data for single columns of data. This is often called the marginal distribution of each column.
                """)
        column_quality_report_info = gr.DataFrame( interactive=False, label="Column Quality Report Summary")

        with gr.Row():
            gr.Markdown("### About the KSComplement:")
            gr.Markdown(r"""
                This neasures the similarity between the continous feature distributions in the original and synthetic data. It's the complement of the Kolmogorov-Smirnov (KS) statistic, so higher values mean better similarity.
                """)

            gr.Markdown("### About the TVComplement:")
            gr.Markdown(r"""
                This measures how well categorical distributions match between the original and synthetic data. It's the complement of Total Variation(TV) distance, so a higher score here also means closer alignment.
                """)
            
        # Spacer (empty HTML element with padding)
        gr.HTML('<div style="height: 30px;"></div>') 
        # Spacer (empty HTML element with padding)
        gr.HTML('<div style="height: 30px;"></div>') 
        gr.Markdown(r"""
                -> The statistical similarity between the real and synthetic data for pairs of columns. This is often called the correlation or bivariate distributions of the columns.
                """)
        
        column_pair_info = gr.DataFrame( interactive=False, label="Column Pair Trends")
        # Spacer (empty HTML element with padding)
        gr.HTML('<div style="height: 30px;"></div>') 
        # Spacer (empty HTML element with padding)
        gr.HTML('<div style="height: 60px;"></div>') 

        gr.Markdown(r"""
                -> Basic validity checks for each of the columns:

                    1) Primary keys must always be unique and non-null

                    2) Continuous values in the synthetic data must adhere to the min/max range in the real data

                    3) Discrete values in the synthetic data must adhere to the same categories as the real data.
                """)
        data_validity_info = gr.DataFrame( interactive=False, label="Data Validity Report")

        # Spacer (empty HTML element with padding)
        gr.HTML('<div style="height: 60px;"></div>') 
        gr.Markdown(r"""
                -> Checks to ensure the real and synthetic data have the same column names
                """)
        data_structure_info = gr.DataFrame( interactive=False, label="Data Structure Report Summary")

        dropdown2.change(process_selection2, inputs=[dropdown1, dropdown2,number_input2], outputs=[output_csv2, column_quality_report_info,column_pair_info,data_validity_info,data_structure_info,df_display21,df_display22,real_data_row_column2,synthetic_data_row_column2])   
        dropdown_options_for_first_tab.change(process_selection1, inputs=[dropdown_options_for_first_tab,number_input1], outputs=[output_csv1, column_quality_report_info,column_pair_info,data_validity_info,data_structure_info,df_display11,df_display12,real_data_row_column1,synthetic_data_row_column1])   
    with gr.Tab("Visualization"):
        #plot
        gr.Markdown("### This can help you see what kind of patterns the synthetic data has learned, and identify differences between the real and synthetic data.")
        gr.Markdown("""
               ### ->Use this function to visualize a real column against the same synthetic column. You can plot any column of type: boolean, categorical, datetime or numerical. 
                """)
    #Textbox for user input to determine x and y columns for the plot
        text_input = gr.Textbox(label="Input Column name")
    # Update plot based on text input
    # Plot display element
        submit_button1 = gr.Button("Submit")
        plot_display = gr.Plot(label="Plot for Column")

        submit_button1.click(lambda text: plot_from_text(text, dataset_instance), inputs=text_input, outputs=plot_display)
        # Spacer (empty HTML element with padding)
        gr.HTML('<div style="height: 80px;"></div>') 
        gr.Markdown("""
               ### ->Use this utility to visualize the trends between a pair of columns for real and synthetic data. You can plot any 2 columns of type: boolean, categorical, datetime or numerical. The columns need not be of the be the same type.
                """)
    #plot for column_pair
        text_input1 = gr.Textbox(label="Input Column1")
        text_input2 = gr.Textbox(label="Input Column2")
        text_input3 = gr.Textbox(label="Input Column2")
        submit_button2 = gr.Button("Submit")
        plot_display1 = gr.Plot(label="Plot for Column Triplet")
        submit_button2.click(lambda text1,text2,text3: plot_from_text2(text1,text2,text3, dataset_instance), inputs=[text_input1,text_input2,text_input3], outputs=plot_display1)

# Launch the Gradio app
demo.launch()
