import os
import re
import subprocess
import camelot
import numpy as np
import pandas as pd
import pikepdf
from tqdm import tqdm

os.chdir('C:/Users/DataMicron/Desktop/Bank_Statement_Reader/')

# input_path_cimb = 'raw_dataset\\cimb\\'
input_path_mayb = 'raw_dataset\\mayb\\'

# cimb_files = sorted(os.listdir(input_path_cimb))
mayb_files = sorted(os.listdir(input_path_mayb))

# output_path_cimb = 'prediction\\2. transaction_output\\cimb\\'
output_path_mayb = 'prediction\\2. transaction_output\\mayb\\'


# if not os.path.exists(output_path_cimb):
#     os.makedirs(output_path_cimb)

if not os.path.exists(output_path_mayb):
    os.makedirs(output_path_mayb)

# for i, pdf in tqdm(enumerate(cimb_files)):
#     file = pikepdf.open(input_path_cimb + pdf, allow_overwriting_input=True)
#     file.save(input_path_cimb + pdf)

for i, pdf in tqdm(enumerate(mayb_files)):
    file = pikepdf.open(input_path_mayb + pdf, allow_overwriting_input=True)
    file.save(input_path_mayb + pdf)

# for i, pdf in tqdm(enumerate(cimb_files)):
#         table = camelot.read_pdf(input_path_cimb + pdf, pages='all', flavor='lattice')
#         tables = pd.DataFrame()
#         with pd.ExcelWriter(output_path_cimb + 'transaction_' + pdf[:-4] + '.xlsx', engine='xlsxwriter') as writer:
#             tables = pd.DataFrame()
#             for x in range(len(table)):
#                 if x == 0:
#                     tables = tables.append(table[0].df)
#                 elif table[0].df[0][0] == table[x].df[0][0]:
#                     tables = tables.append(table[x].df.iloc[1:])
#             tables = tables.reset_index().drop(columns=['index'], axis=1)
#
#             columns = tables[0][0].split("\n")
#             columns = columns[:7]
#
#             dates = []
#             descriptions = []
#             refs = []
#             withdraws = []
#             deposits = []
#             taxes = []
#             balances = []
#             for i in range(2, len(tables)):
#
#                 # Get date & description
#                 # ----------------------------------------
#                 date = tables[0][i][:10]
#                 description = tables[0][i][12:]
#                 add_description = tables[1][i]
#                 ref = tables[2][i]
#                 # ----------------------------------------
#
#                 # Get withdrawal (debit)
#                 # ----------------------------------------
#                 withdraw = re.sub(',', '', tables[3][i])
#                 if withdraw == '':
#                     withdraw = 0
#                 else:
#                     withdraw = float(withdraw)
#                 # ----------------------------------------
#
#                 # Get deposit (credit)
#                 # ----------------------------------------
#                 deposit = re.sub(',', '', tables[4][i])
#                 if deposit == '':
#                     deposit = 0
#                 else:
#                     deposit = float(deposit)
#                 # ----------------------------------------
#
#                 # Get tax
#                 # ----------------------------------------
#                 tax = re.sub(',', '', tables[5][i])
#                 if tax == '':
#                     tax = 0
#                 else:
#                     tax = float(tax)
#                 # ----------------------------------------
#
#                 # Get account balance
#                 # ----------------------------------------
#                 balance = re.sub(',', '', tables[6][i])
#                 if balance == '':
#                     balance = 0
#                 else:
#                     balance = float(balance)
#                 # ----------------------------------------
#
#                 # Append all lists
#                 # ----------------------------------------
#                 dates.append(date)
#                 descriptions.append(description + '\n' + add_description)
#                 refs.append(ref)
#                 withdraws.append(withdraw)
#                 deposits.append(deposit)
#                 taxes.append(tax)
#                 balances.append(balance)
#                 # ----------------------------------------
#
#             transactions_df = pd.DataFrame(list([dates, descriptions, refs, withdraws, deposits, taxes, balances])).T
#             transactions_df.columns = columns
#             transactions_df.to_excel(writer, sheet_name='transactions', index=False)


for i, pdf in tqdm(enumerate(mayb_files)):

        table = camelot.read_pdf(input_path_mayb + pdf, pages='all', flavor='stream')
        tables = pd.DataFrame()
        with pd.ExcelWriter(output_path_mayb + 'transaction_' + pdf[:-4] + '.xlsx', engine='xlsxwriter') as writer:

            table = camelot.read_pdf(input_path_mayb + pdf, pages='all', flavor='lattice')

            tables = pd.DataFrame()
            for x in range(len(table)):
                if x == 0:
                    tables = tables.append(table[0].df)
                elif x != 0:
                    tables = tables.append(table[x].df.iloc[1:])
            tables = tables.reset_index().drop(columns=['index'], axis=1)
            tables1 = tables.iloc[1:].reset_index().drop(columns=['index'], axis=1)

            for i in range(len(tables.columns)):
                multi_row_column = tables.iloc[:, i].to_list()
                tables1[0][i] = '\n'.join(multi_row_column)

            tables1 = tables1.iloc[:1]
            tables1.columns = tables.iloc[0]

            columns = tables.iloc[0, :]

            dates = []
            descs = []
            trans = []
            balances = []

            for i in range(1, len(tables)):
                value = tables.iloc[i, :]

                date = value[0].split("\n")
                description = value[1].split("\n")
                transaction = value[2].split("\n")
                balance = value[3].split("\n")

                dates.extend(date)
                descs.extend(description)
                trans.extend(transaction)
                balances.extend(balance)

            descriptions = []
            for i in range(len(descs)):
                if re.search("   ", descs[i]) != None:
                    descriptions[-1] = descriptions[-1] + descs[i]
                else:
                    descriptions.append(descs[i])
            descriptions = descriptions[1:]

            for i in range(len(descriptions)):
                try:
                    if (descriptions[i][:22] == 'PAYMENT VIA MYDEBIT   ') and (len(descriptions[i].split('   ')) == 3):
                        descriptions[i] = descriptions[i] + ('   ') + descriptions[i + 1]
                        del descriptions[i + 1]
                    elif (descriptions[i][:19] == 'FUND TRANSFER TO A/') and (len(descriptions[i].split('   ')) == 3):
                        descriptions[i] = descriptions[i] + ('   ') + descriptions[i + 1]
                        del descriptions[i + 1]

                    elif (descriptions[i][:20] == 'FPX PAYMENT FR A/   ') and (
                            len(descriptions[i].split('   ')) == 3) or (len(descriptions[i].split('   ')) == 2):
                        descriptions[i] = descriptions[i] + ('   ') + descriptions[i + 1]
                        del descriptions[i + 1]

                    elif (descriptions[i] == 'ENDING BALANCE :'):
                        del descriptions[i:]
                except:
                    pass

            trans = trans[:-3]
            balances = balances[1:]
            df = pd.DataFrame((dates, descriptions, trans, balances)).T
            df.columns = columns
            df = df.dropna()

            df['CREDIT'] = 0
            df['DEBIT'] = 0

            for i in range(len(df)):
                if df[df.columns[2]][i].find('+') != -1:
                    df['CREDIT'][i] = re.sub(r'[,+-]+', r'', df[df.columns[2]][i])
                    df['DEBIT'][i] = 0
                    df[df.columns[3]][i] = re.sub(r',', r'', df[df.columns[3]][i])

                elif df[df.columns[2]][i].find('-') != -1:
                    df['DEBIT'][i] = re.sub(r'[,+-]+', r'', df[df.columns[2]][i])
                    df['CREDIT'][i] = 0
                    df[df.columns[3]][i] = re.sub(r',', r'', df[df.columns[3]][i])

            df[df.columns[3]] = df[df.columns[3]].astype('float')
            df['DEBIT'] = df['DEBIT'].astype('float')
            df['CREDIT'] = df['CREDIT'].astype('float')

            df.to_excel(writer, sheet_name='transactions', index=False)



