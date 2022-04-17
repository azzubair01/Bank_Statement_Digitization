import pandas as pd
import os
import glob
import re
import subprocess
from tqdm import tqdm

input_path = 'C:\\Users\\DataMicron\\Desktop\\Bank_Statement_Reader\\financial_output\\mayb\\'
file_list = glob.glob1(input_path,"*.xlsx")
output_path = 'C:\\Users\\DataMicron\\Desktop\\Bank_Statement_Reader\\extract_description\\raw_files\\'

if not os.path.exists(output_path):
    subprocess.call("powershell mkdir " + output_path)

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
            pattern2 = re.search('[*]', df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i])
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
            pattern2 = re.search('[*]', df_transaction['BUTIR URUSNIAGA\n進支項說明\nTRANSACTION DESCRIPTION'][i])
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
    df_final.to_excel(output_path + 'output2_' + file_list[j][7:], index=False)