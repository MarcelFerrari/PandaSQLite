import pandas as pd


def export_df_to_all_formats():
    # Define test data
    df = pd.DataFrame({'col1': [1, 2, 3],
                       'col2': ['a', 'b', 'c'],
                       'col3': [True, False, True]})
    
    # Define file names for each format
    file_names = {'csv': 'test.csv',
                  'fwf': 'test.fwf',
                  'excel': 'test.xlsx',
                  'json': 'test.json',
                  'parquet': 'test.parquet',
                  'stata': 'test.dta',
                  'html': 'test.html',
                  'feather': 'test.feather',
                  'msgpack': 'test.msgpack',
                  'pickle': 'test.pickle',
                  'sql': 'test.sql',
                  'gbq': 'test.gbq',
                  'excel': 'test.xlsx'}
    
    # Export to all formats
    for fmt, file_name in file_names.items():
        if fmt == 'csv':
            df.to_csv(file_name, index=False)
        elif fmt == 'excel':
            df.to_excel(file_name, index=False)
        elif fmt == 'json':
            df.to_json(file_name, orient='records')
        elif fmt == 'parquet':
            df.to_parquet(file_name, engine='auto', compression='snappy')
        elif fmt == 'stata':
            df.to_stata(file_name, write_index=False)
        elif fmt == 'html':
            df.to_html(file_name, index=False)
        elif fmt == 'feather':
            df.to_feather(file_name)
        elif fmt == 'pickle':
            df.to_pickle(file_name)
    
    print('Dataframe exported to all formats.')

if __name__ == "__main__":
    export_df_to_all_formats()