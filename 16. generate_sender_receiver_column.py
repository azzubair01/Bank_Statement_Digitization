import pandas as pd
import os
import glob
import re
import subprocess
from tqdm import tqdm

os.chdir('C:/Users/DataMicron/Desktop/Bank_Statement_Reader/')

input_path = 'prediction\\4. financial_output\\mayb\\'
file_list = glob.glob1(input_path,"*.xlsx")
output_path = 'prediction\\5. extract_description\\raw_files\\'

if not os.path.exists(output_path):
    os.makedirs(output_path)

index = 1
for j in tqdm(range(len(file_list))):

    df_transaction = pd.read_excel(input_path + file_list[j], sheet_name='transactions')
    df_metadata = pd.read_excel(input_path + file_list[j], sheet_name='metadata')
    df_metadata['Value'] = df_metadata['Value'].str.replace('\n_x000C_', '')

    senders = []
    receivers = []

    for i in tqdm(range(len(df_transaction))):
        if re.search('SVG GIRO CR', df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i]) != None:
            pattern = re.search('SVG GIRO CR', df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i])
            description_text = df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i]
            entity = description_text[pattern.span()[1]:]

        elif re.search('SALE DEBIT', df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i]) != None:
            entity = 'ONLINE DEBIT'
            # entity = ''

        elif re.search('DEBIT ADVICE', df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i]) != None:
            entity = 'BANK DEDUCTION'
            # entity = ''

        elif re.search('CASH WITHDRAWAL', df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i]) != None:
            entity = 'ATM WITHDRAWAL'
            # entity = ''

        elif re.search('IBK FUND TFR FR A/C',
                       df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i]) != None:
            pattern1 = re.search('IBK FUND TFR FR A/C',
                                 df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i])
            pattern2 = re.search('[*]', df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i])
            description_text = df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i]
            entity = description_text[pattern1.span()[1]:pattern2.span()[0]]
            # entity = ''

        elif re.search('CLEARING CHQ DEP',
                       df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i]) != None:
            entity = 'SALARY INCOME'
            # entity = ''

        elif re.search('TRANSFER FROM A/C',
                       df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i]) != None:
            pattern1 = re.search('TRANSFER FROM A/C',
                                 df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i])
            pattern2 = re.search('[*]|TABUNG HAJI TRF|', df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i])
            description_text = df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i]
            entity = description_text[pattern1.span()[1]:pattern2.span()[0]]
            # entity = ''

        elif re.search('PAYMENT VIA MYDEBIT',
                       df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i]) != None:
            pattern1 = re.search('PAYMENT VIA MYDEBIT',
                                 df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i])
            pattern2 = re.search('[*]', df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i])
            description_text = df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i]
            entity = description_text[pattern1.span()[1]:]
            # entity = ''

        elif re.search('FUND TRANSFER TO A/',
                       df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i]) != None:
            pattern1 = re.search('FUND TRANSFER TO A/',
                                 df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i])
            pattern2 = re.search('[*]', df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i])
            description_text = df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i]
            entity = description_text[pattern1.span()[1]:]
            # entity = ''

        elif re.search('FPX PAYMENT FR A/',
                       df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i]) != None:
            # entity_list = df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i].split('   ')
            # print(entity_list)
            # entity = entity_list[2]
            pattern1 = re.search('[*]', df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i])
            pattern2 = re.search('[0-9]+', df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i][
                                           pattern1.span()[1]:])
            description_text = df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i]
            entity = description_text[pattern1.span()[1]:]
            # entity = ''

        elif re.search('FUND TRANSFER TO',
                       df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i]) != None:
            pattern1 = re.search('FUND TRANSFER TO',
                                 df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i])
            pattern2 = re.search('[*]', df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i])
            description_text = df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i]
            entity = description_text[pattern1.span()[1]:]
            # entity = ''

        elif re.search('IBK FUND TFR TO A/C',
                       df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i]) != None:
            pattern1 = re.search('IBK FUND TFR TO A/C',
                                 df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i])
            pattern2 = re.search('[*]', df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i])
            description_text = df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i]
            entity = description_text[pattern1.span()[1]:pattern2.span()[0]]
            # entity = ''

        elif re.search('PYMT FROM A/C', df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i]) != None:
            pattern1 = re.search('PYMT FROM A/C', df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i])
            pattern2 = re.search('[*]|', df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i])

            if pattern2.span()[1] == 0:
                entity = 'PAYMENT FROM MYSELF'

            else:
                description_text = df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i]
                entity = description_text[pattern1.span()[1]:pattern2.span()[0]]
            # entity = ''

            description_text = df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i]
            entity = description_text[pattern1.span()[1]:pattern2.span()[0]]
            # entity = ''

        elif re.search('HIBAH PAID', df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i]) != None:
            pattern1 = re.search('HIBAH PAID', df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i])
            entity = 'INSURANCE HIBAH'
            # entity = ''

        elif re.search('CASH DEPOSIT', df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i]) != None:
            pattern1 = re.search('CASH DEPOSIT', df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i])
            entity = 'ATM DEPOSIT'
            # entity = ''

        else:
            entity = ''

        if df_transaction['CREDIT'][i] != 0:
            sender = str(entity)
            receiver = df_metadata[df_metadata['Key'] == 'account_holder']['Value'].values[0]
        else:
            sender = df_metadata[df_metadata['Key'] == 'account_holder']['Value'].values[0]
            receiver = str(entity)

        senders.append(sender)
        receivers.append(receiver)

    df_new = pd.DataFrame({'SENDER': senders, 'RECEIVER': receivers})
    df_final = pd.concat([df_transaction, df_new], axis=1)
    df_final.columns = ['TARIKH MASUK', 'BUTIR URUSNIAGA', 'JUMLAH URUSNIAGA', 'BAKI PENYATA', 'KREDIT', 'DEBIT', 'PEMBERI', 'PENERIMA']

    df_final['ID TRANSAKSI'] = ''

    for i in range(len(df_final)):
        df_final['ID TRANSAKSI'][i] = 'T00' + str(index)
        index += 1
        df_final['JUMLAH URUSNIAGA'][i] = re.sub('[+,-]', '', df_final['JUMLAH URUSNIAGA'][i])

    df_final['TARIKH MASUK'] = pd.to_datetime(df_final['TARIKH MASUK'], infer_datetime_format=True)


    df_final['JUMLAH URUSNIAGA'] = df_final['JUMLAH URUSNIAGA'].astype('float')

    df_final['BAKI PENYATA'] = df_final['BAKI PENYATA'].astype('float')
    df_final['KREDIT'] = df_final['KREDIT'].astype('float')
    df_final['DEBIT'] = df_final['DEBIT'].astype('float')

    df_final['PEMBERI'] = df_final['PEMBERI'].astype('str')
    df_final['PENERIMA'] = df_final['PENERIMA'].astype('str')

    df_final = df_final[['ID TRANSAKSI', 'TARIKH MASUK', 'BUTIR URUSNIAGA', 'JUMLAH URUSNIAGA', 'BAKI PENYATA', 'KREDIT', 'DEBIT',
                        'PEMBERI', 'PENERIMA']]

    # df_final.to_excel(output_path + 'output2_' + file_list[j][7:], index=False)
    df_final.to_csv(output_path + 'output2_' + file_list[j][7:-5] + '.csv', index=False)