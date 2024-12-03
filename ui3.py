import gradio as gr
import pandas as pd
from single_table import get_column_pair_plot,get_column_plot,get_column_triple_plot,get_column_quad_plot
import shutil,os
from upload import process_csv

# Define the folder to save uploaded CSV files
SAVE_FOLDER = "my_folder"

class Dataset:
    def initialize(self, data, metadata, synthetic_data):
        self.real_data = data
        self.metadata = metadata
        self.synthetic_data = synthetic_data

# Define dataset_instance as a global variable
dataset_instance = Dataset()


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
    data,metadata=process_csv()
    synthetic_data=None
    dataset_instance.initialize(data, metadata, synthetic_data)
    
    return data.shape,data

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
def plot_from_text1(column1,column2,dataset_instance):
    #fig = px.scatter(df, x=df.columns[0], y=df.columns[1], title="Synthetic Data Scatter Plot")
    fig = get_column_pair_plot(
        real_data=dataset_instance.real_data,
        synthetic_data=None,
        metadata=dataset_instance.metadata,
        column_names=[f"{column1}",f"{column2}"]
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

def plot_from_text3(column1,column2,column3,column4,dataset_instance):
    fig = get_column_quad_plot(
        real_data=dataset_instance.real_data,
        synthetic_data=None,
        metadata=dataset_instance.metadata,
        column_names=[f"{column1}",f"{column2}",f"{column3}",f"{column4}"]
        )
    return fig


# Create the Gradio Interface with 3 tabs
with gr.Blocks() as demo:
    with gr.Tab("Upload your own Dataset"):
        with gr.Row():
            with gr.Row():
                
                file_input = gr.File(label="Upload your CSV file")
                submit_btn = gr.Button("Upload")

            with gr.Row():
            
                real_data_row_column1=gr.Textbox(label="Rows and columns in Real Data",interactive=False)

            # DataFrame display element
            with gr.Row():
                df_display1 = gr.DataFrame(label="Data Preview", interactive=False)
                
                
            submit_btn.click(save_csv_in_a_folder, inputs=file_input,outputs=[real_data_row_column1,df_display1])
        
        delete_datasets_button = gr.Button("Delete Uploaded Datasets")
        
        delete_datasets_button.click(delete_all_files_in_folder)
    
    with gr.Tab("Visualization Intelligence"):
    #Textbox for user input to determine x and y columns for the plot
        text_input = gr.Textbox(label="Input Column name")
    # Update plot based on text input
    # Plot display element
        submit_button1 = gr.Button("Submit")
        plot_display = gr.Plot(label="Plot for Column")

        submit_button1.click(lambda text: plot_from_text(text, dataset_instance), inputs=text_input, outputs=plot_display)
        # Spacer (empty HTML element with padding)
        gr.HTML('<div style="height: 80px;"></div>') 
    #plot for column_pair
        text_input1 = gr.Textbox(label="Input Column1")
        text_input2 = gr.Textbox(label="Input Column2")
        submit_button2 = gr.Button("Submit")
        plot_display1 = gr.Plot(label="Plot for Column Pair")
        submit_button2.click(lambda text1,text2: plot_from_text1(text1,text2, dataset_instance), inputs=[text_input1,text_input2], outputs=plot_display1)

    with gr.Tab("Column triplets"):
        text_input3 = gr.Textbox(label="Input Column1")
        text_input4 = gr.Textbox(label="Input Column2")
        text_input5 = gr.Textbox(label="Input Column3 (Scaling Column)")
        submit_button3 = gr.Button("Submit")
        plot_display2 = gr.Plot(label="Plot for Column Triplet")
        submit_button3.click(lambda text1,text2,text3: plot_from_text2(text1,text2,text3, dataset_instance), inputs=[text_input3,text_input4,text_input5], outputs=plot_display2)

    with gr.Tab("Column quads"):
        text_input6 = gr.Textbox(label="Input Column1")
        text_input7 = gr.Textbox(label="Input Column2")
        text_input8 = gr.Textbox(label="Input Column3")
        text_input9 = gr.Textbox(label="Input Column4 (Scaling Column)")
        submit_button4 = gr.Button("Submit")
        plot_display3 = gr.Plot(label="Plot for Column Quad")
        submit_button4.click(lambda text1,text2,text3,text4: plot_from_text3(text1,text2,text3,text4, dataset_instance), inputs=[text_input6,text_input7,text_input8,text_input9], outputs=plot_display3)

# Launch the Gradio app
demo.launch()
