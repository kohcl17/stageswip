import streamlit as st
import pandas as pd
from helper_functions.date_gene import qc_df

class FileUploads():
    def read_xfile(self, df_query):
        '''
        Parameter
        ---------
        df_query: from the st.file_uploader output

        Returns
        -------

        dict| keys as names of file, values as pd DataFrame, cleaned for date-gene terms
        '''

        df_dict = {}
        for d in df_query:
            head, sep, tail = str(d.name).partition(".")
            if tail == 'csv':
                data = pd.read_csv(d, index_col=0)
                df_dict[head] = data

            elif tail == 'txt':
                data = pd.read_csv(d, sep='\t', index_col=0)
                df_dict[head] = data

            elif tail == 'xlsx':
                x = st.cache_data(pd.read_excel)(d, index_col=0, sheet_name=None, engine='openpyxl')
                selected_sheet = file_opts.multiselect(label="* Select which sheet to read in", options=x.keys())
                if len(selected_sheet) != 0:
                    for i in selected_sheet:
                        df_dict[f"{head}_{i}"] = x[i]
                else:
                    st.stop()
        
        return df_dict
    
    def capslock_genes(self, df_dict):
        for df in df_dict.values():
            df.index = df.index.astype(str, copy=False) # expand to format actual dates from excel sheets as text
            df.index = df.index.str.upper()

        cleandict = qc_df(df_dict)

        return cleandict
    
    
fileuploads = FileUploads()