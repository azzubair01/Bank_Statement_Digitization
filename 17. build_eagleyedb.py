import pandas as pd
import numpy as np
import glob
import os
import subprocess
from tqdm import tqdm

# file_list = glob.glob1('C:\\Users\\DataMicron\\Desktop\\Bank_Statement_Reader\\extract_description\\raw_files\\', '*.xlsx')
input_path = 'C:\\Users\\DataMicron\\Desktop\\Bank_Statement_Reader\\extract_description\\edited_files\\'
file_list = glob.glob1(input_path, '*.xlsx')
output_path = 'C:\\Users\\DataMicron\\Desktop\\Bank_Statement_Reader\\eagleyedb\\'

if not os.path.exists(output_path):
    subprocess.call("powershell mkdir " + output_path)

def flatten(list_of_list):
    return [item for sublist in list_of_list for item in sublist]


def get_entity_type_id(datalake_df):
    entity_type_id = []
    for i in range(len(datalake_df.columns)):
        column_index_no = datalake_df.columns.get_loc(datalake_df.columns[i]) + 1
        entity_type_id.append(column_index_no)
    return entity_type_id


def get_entity_type(datalake_df):
    datalake_df.columns = map(str.upper, datalake_df.columns)
    entity_type = datalake_df.columns.to_list()
    return entity_type


def get_entity_desc(entity_type):
    entity_type_desc = entity_type.copy()
    return entity_type_desc


def get_entity(datalake_df):
    entities = flatten(datalake_df.values.tolist())
    return entities


def get_entity_id(entities):
    entity_ids = []
    for i in range(len(entities)):
        entity_id = i + 1
        entity_ids.append(entity_id)
    return entity_ids


def get_factor(entity_id, entity_type):
    factor = len(entity_id) / len(entity_type)
    return int(factor)


def get_factor2(entity_id):
    factor = len(entity_id)
    return int(factor)


def get_entity_type2(entity_id, entity_type_id):
    entity_type = entity_type_id.copy()
    factor = get_factor(entity_id, entity_type)
    entity_type = entity_type_id.copy() * factor
    return entity_type


def get_location(factor):
    locations = ['' for i in range(factor)]
    return locations


def get_address(factor):
    addresses = ['' for i in range(factor)]
    return addresses


def get_image(entity_type):
    images = []
    image = ''
    for i in range(len(entity_type)):
        if entity_type[i] == 1:
            image = '/assets/images/money.png'
        elif entity_type[i] == 2:
            image = '/assets/images/person.png'
        elif entity_type[i] == 3:
            image = '/assets/images/person.png'
        else:
            pass
        images.append(image)
    return images


def get_doc_id(factor):
    doc_ids = [1 for i in range(factor)]
    return doc_ids


def get_search_around(entity_type):
    searcharounds = []
    for i in range(len(entity_type)):
        if entity_type[i] == 1:
            searcharound = ''
        elif entity_type[i] == 2:
            searcharound = ''
        elif entity_type[i] == 3:
            searcharound = ''
        searcharounds.append(searcharound)
    return searcharounds


def get_search_around_url(factor):
    search_around_url = ['' for i in range(factor)]
    return search_around_url


def get_event_name():
    event_name = ['send', '']
    return event_name


def get_event_desc(event_name):
    event_desc = event_name.copy()
    return event_desc


def get_event_id(event_name):
    event_ids = []
    for i in range(len(event_name)):
        event_id = i + 1
        event_ids.append(event_id)
    return event_ids


def random_dates(start, end, n=1):
    start_u = start.value // 10 ** 9
    end_u = end.value // 10 ** 9
    return pd.to_datetime(np.random.randint(start_u, end_u, n), unit='s')


def get_doc_id2(entity_id):
    docids = [1 for i in range(len(entity_id))]
    return docids


def get_entity_id2(entity_id):
    entityids = entity_id.copy()
    return entityids


def get_start_idx(entity_id):
    start_idx = [0 for i in range(len(entity_id))]
    return start_idx


def get_end_idx(entity_id):
    end_idx = [5 for i in range(len(entity_id))]
    return end_idx


def get_date(dates_df):
    dates_list = []
    for i in range(len(dates_df)):
        date = dates_df['TARIKH MASUK'][i]
        for j in range(3):
            dates_list.append(date)
    return dates_list


def get_date2(dates_df):
    dates_list = []
    for i in range(len(dates_df)):
        date = dates_df['TARIKH MASUK'][i]
        for j in range(3 - 1):
            dates_list.append(date)
    return dates_list


def get_entity_unique_id(docid, entity_id, start_idx, end_idx):
    df = pd.DataFrame([docid, entity_id, start_idx, end_idx]).T
    df.columns = ['docid', 'entityid', 'startidx', 'endidx']
    df['entityuniqueid'] = ''
    for i in range(len(df)):
        df['entityuniqueid'][i] = int(
            str(df['docid'][i]) + str(df['entityid'][i]) + str(df['startidx'][i] + df['endidx'][i]))
    entityuniqueid = df['entityuniqueid'].to_list()
    return entityuniqueid


def get_relations(entity_df, entity_mentions_df):
    merged_df = entity_df.merge(entity_mentions_df, left_on='EntityId', right_on='EntityId')

    # -----------------------------------------------------------------------------------

    # Replace entityuniqueid of similar entities
    filtered_df = merged_df[~merged_df['EntityType'].isin([6, 9, 10, 11, 12])].dropna(subset=['EntityName'])
    duplicated_df2 = filtered_df[filtered_df.duplicated(subset=['EntityName'])]
    sorted_df2 = duplicated_df2.sort_values(ascending=True, by='EntityName').reset_index(drop=True)
    for j in range(1, len(sorted_df2)):
        if sorted_df2['EntityName'][j] == sorted_df2['EntityName'][j - 1]:
            sorted_df2['EntityUniqueId'][j] = sorted_df2['EntityUniqueId'][j - 1]
        else:
            sorted_df2['EntityUniqueId'][j] = sorted_df2['EntityUniqueId'][j]
    for i in range(len(sorted_df2)):
        for j in range(len(merged_df)):
            if sorted_df2['EntityName'][i] == merged_df['EntityName'][j]:
                merged_df['EntityUniqueId'][j] = sorted_df2['EntityUniqueId'][i]

    # Split entity by entity id
    entity_type1_df = merged_df[merged_df['EntityType'] == 1].reset_index(drop=True)
    entity_type2_df = merged_df[merged_df['EntityType'] == 2].reset_index(drop=True)
    entity_type3_df = merged_df[merged_df['EntityType'] == 3].reset_index(drop=True)

    # -----------------------------------------------------------------------------------

    # Map Relations based on their entity type
    entity1ids = []
    entity2ids = []
    entity1dtypes = []
    entity2dtypes = []

    entity1d = entity_type2_df['EntityUniqueId'].tolist()
    entity1dtype = entity_type2_df['EntityType'].tolist()
    entity1ids.extend(entity1d)
    entity1dtypes.extend(entity1dtype)
    entity2d = entity_type1_df['EntityUniqueId'].tolist()
    entity2dtype = entity_type1_df['EntityType'].tolist()
    entity2ids.extend(entity2d)
    entity2dtypes.extend(entity2dtype)

    entity1d = entity_type1_df['EntityUniqueId'].tolist()
    entity1dtype = entity_type1_df['EntityType'].tolist()
    entity1ids.extend(entity1d)
    entity1dtypes.extend(entity1dtype)
    entity2d = entity_type3_df['EntityUniqueId'].tolist()
    entity2dtype = entity_type3_df['EntityType'].tolist()
    entity2ids.extend(entity2d)
    entity2dtypes.extend(entity2dtype)

    # -----------------------------------------------------------------------------------

    return entity1ids, entity2ids, entity1dtypes, entity2dtypes, merged_df


def get_columns():
    columns = ['DocId', 'Entity1Id', 'Entity2Id', 'Entity1Type', 'Entity2Type', 'Date']
    return columns


def get_columns2():
    columns = ['DocId', 'EventId', 'Entity1Id', 'Entity2Id', 'Date']
    return columns


def get_event_id2(event_mentions_df):
    event_ids = []
    event_id = ''
    for i in range(len(event_mentions_df)):
        if event_mentions_df['Entity2Type'][i] == 2:
            event_id = 1
        elif event_mentions_df['Entity2Type'][i] == 3:
            event_id = 1
        else:
            event_id = 1
        event_ids.append(event_id)
    return event_ids


def clean_na(event_mentions_df2, merged_df):
    column_name = event_mentions_df2.columns.to_list()
    working_df = event_mentions_df2.merge(merged_df, left_on='Entity2Id', right_on='EntityUniqueId',
                                          suffixes=('', '_x'))
    working_df = working_df.dropna(subset=['EntityName'])
    working_df = working_df[working_df['EntityName'] != ''].reset_index(drop=True)
    working_df2 = working_df[column_name]
    return working_df2, working_df


def get_relations3(connected_entity_df, event_mentions_df2):
    column_name = event_mentions_df2.columns.to_list()
    connected_entity_df = connected_entity_df[connected_entity_df.duplicated(subset='EntityName', keep=False)]
    connected_entity_df['Entitiy1Id_copy'] = connected_entity_df['Entity1Id']
    connected_entity_df['Entitiy2Id_copy'] = connected_entity_df['Entity2Id']
    connected_entity_df['Entity1Id'] = connected_entity_df['Entitiy2Id_copy']
    connected_entity_df['Entity2Id'] = connected_entity_df['Entitiy1Id_copy']
    connected_entity_df['EventId'] = 2
    connected_entity_df = connected_entity_df[column_name]
    event_mentions_df2 = event_mentions_df2.append(connected_entity_df)
    event_mentions_df2 = event_mentions_df2.drop_duplicates(subset=['Entity1Id', 'Entity2Id']).reset_index(drop=True)

    return event_mentions_df2



# Append all excel files into a single table
datalake_df = pd.DataFrame()
dates_df = pd.DataFrame()
for i in tqdm(range(len(file_list))):
    # Read the Input database
    transaction_df = pd.read_excel(input_path + file_list[i])[['JUMLAH URUSNIAGA', 'SENDER', 'RECEIVER']]
    datalake_date = pd.read_excel(input_path + file_list[i])[['TARIKH MASUK']]
    datalake_df = datalake_df.append(transaction_df,ignore_index=True)
    dates_df = dates_df.append(datalake_date,ignore_index=True)

# Clean column 'JUMLAH URUSNIAGA'
datalake_df['JUMLAH URUSNIAGA'] = datalake_df['JUMLAH URUSNIAGA'].str.replace('+', '')
datalake_df['JUMLAH URUSNIAGA'] = datalake_df['JUMLAH URUSNIAGA'].str.replace('-', '')
datalake_df['JUMLAH URUSNIAGA'] = datalake_df['JUMLAH URUSNIAGA'].str.replace(',', '')
datalake_df['JUMLAH URUSNIAGA'] = datalake_df['JUMLAH URUSNIAGA'].astype('float')
datalake_df['JUMLAH URUSNIAGA'] = datalake_df['JUMLAH URUSNIAGA'].apply(lambda x: f"RM {x}")

# Transpose Documents from Datalake into EagleyeDB
column_name = ['DocId','DocName','DocLocation','Date','Text']
document_df = pd.DataFrame({column_name[0]:[1], column_name[1]:['AUDIT DATABASES'],column_name[2]:['AUDIT SYSTEM/DATABASES'],
                            column_name[3]:['1/1/2022  12:00:00 AM'],column_name[4]:[' ']})
document_df['Date'] = document_df['Date'].astype('datetime64')

# Transpose Entity Type from Datalake into EagleyeDB
column_name = ['TypeId', 'TypeName', 'TypeDescription']
entity_type = get_entity_type(datalake_df)
entity_type_desc = get_entity_desc(entity_type)
entity_type_id = get_entity_type_id(datalake_df)
entity_type_df2 = pd.DataFrame([entity_type_id, entity_type, entity_type_desc]).T
entity_type_df2.columns = column_name
# print(entity_type_df)

# Transpose EntityAttribute from Datalake into Eagle Eye DB
column_name = ['EntityId','AttributeName','AttributeValue','DocId']
entity_attributes_df = pd.DataFrame({column_name[0]:[''],column_name[1]:[''],column_name[2]:[''],column_name[3]:['']})

# Transpose Entities from Datalake into Eagle Eye DB
column_name = ['EntityId','EntityName','EntityType','Location','Address','Image','DocId']
entities = get_entity(datalake_df)
entity_id = get_entity_id(entities)
factor = get_factor2(entity_id)
entity_type2 = get_entity_type2(entity_id, entity_type_id)
location = get_location(factor)
address = get_address(factor)
image = get_image(entity_type2)
doc_id = get_doc_id(factor)
searcharound = get_search_around(entity_type2)
searcharoundurl = get_search_around_url(factor)
entity_df2 = pd.DataFrame([entity_id, entities, entity_type2, location, address, image, doc_id]).T
entity_df2.columns = column_name
entity_df2['EntityName'] = entity_df2['EntityName'].astype('string')
entity_df2 = entity_df2.fillna('')
entity_df2['EntityName'] = entity_df2['EntityName'].str.replace(' 00:00:00', '')
# print(entity_df)


# Transpose Entity Mentions from Datalake into Eagle Eye DB
column_name = ['DocId','EntityId','StartIndex','EndIndex','Date','EntityUniqueId']
doc_id = get_doc_id2(entity_id)
entity_ids = get_entity_id2(entity_id)
start_idx = get_start_idx(entity_id)
end_idx = get_end_idx(entity_id)
date = get_date(dates_df)
entity_unique_id = get_entity_unique_id(doc_id, entity_ids, start_idx, end_idx)
entity_mentions_df2 = pd.DataFrame([doc_id, entity_ids, start_idx, end_idx, date, entity_unique_id]).T
entity_mentions_df2.columns = column_name
entity_mentions_df2['Date'] = entity_mentions_df2['Date'].astype('datetime64')
# print(entity_mentions_df)


# Transpose Event Types from Datalake into Eagle Eye DB
column_name = ['EventId','EventName','EventDescription']
event_name = get_event_name()
event_desc = get_event_desc(event_name)
event_id = get_event_id(event_name)
event_types_df2 = pd.DataFrame([event_id, event_name, event_desc]).T
event_types_df2.columns = column_name
# print(event_types_df2)


# Transpose Event Mentions from Datalake into Eagle Eye DB
entity1id, entity2id, entity_type1d, entity_type2d, merged_df = get_relations(entity_df2, entity_mentions_df2)
doc_id = get_doc_id2(entity1id)
date = get_date2(dates_df)
event_mentions_df2 = pd.DataFrame([doc_id, entity1id, entity2id, entity_type1d, entity_type2d, date]).T
column_name = get_columns()
event_mentions_df2.columns = column_name
event_mentions_df2['Date'] = event_mentions_df2['Date'].astype('datetime64')
event_id = get_event_id2(event_mentions_df2)
event_mentions_df2['EventId'] = event_id
column_name = get_columns2()
event_mentions_df2 = event_mentions_df2[column_name]
# event_mentions_df2


# Auto-connect among entities with attributes
# event_mentions_df2, connected_entity_df = clean_na(event_mentions_df2, merged_df)
# event_mentions_df2 = get_relations3(connected_entity_df, event_mentions_df2)
# print(event_mentions_df2)


# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter(output_path + 'EagleyeSampleDb.xlsx', engine='openpyxl')

# Write each dataframe to a different worksheet.
document_df.to_excel(writer, sheet_name='Documents', index=False)
entity_type_df2.to_excel(writer, sheet_name='EntityTypes', index=False)
entity_df2.to_excel(writer, sheet_name='Entities', index=False)
entity_attributes_df.to_excel(writer, sheet_name='EntityAttributes', index=False)
entity_mentions_df2.to_excel(writer, sheet_name='EntityMentions', index=False)
event_types_df2.to_excel(writer, sheet_name='EventTypes', index=False)
event_mentions_df2.to_excel(writer, sheet_name='EventMentions', index=False)

# Close the Pandas Excel writer and output the Excel file.
writer.save()
