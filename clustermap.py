'''---Import Package---'''
import os
import pandas as pd
import numpy as np
from plot_clustermap import *
from sklearn.preprocessing import StandardScaler

''' datafd: Input File Directory'''

def main(datafd):
    
    datalist = [f for f in os.listdir(datafd) if f.endswith('.xlsx')]

    '''Read Excel'''
    density = []
    cell_type = []
    info = []
    patients_number = []

    for i in range(len(datalist) - 1):
        # 讀取 Excel 文件的內容
        data = pd.read_excel(os.path.join(datafd, datalist[i]),engine='openpyxl')
        info.append(data.iloc[1:, :].values)
        '''
        if data.shape[0] == 11:
            density.append(data.iloc[2:, 4].values)        # 取 density column 的值
            cell_type.append(data.iloc[2:, 0].values)      # 免疫細胞的名稱
            patients_number.append(data.iloc[1, 1])        # 病人編號
        '''

    '''List to Numpy'''
    info = np.concatenate(info, axis=0)
    print('===============================')
    print("Info")
    print(info)
    print(info.shape)
    print('===============================')

    '''---Unique value and index---'''
    cname1, u1a, u2a = np.unique(info[:, 0], return_index=True, return_inverse=True) # cname1 會是所有免疫細胞的名稱 u1a會是他們分別對應到的索引
    cname2, u1b, u2b = np.unique(info[:, 1], return_index=True, return_inverse=True) # cname2 會是所有病人的編號，u1b會是他們分別對應的索引
    print('===============================')
    print("cname1 & canme2")
    print(cname1)
    print(cname2)
    print('===============================')
    print('===============================')
    print("u1a & u1b")
    print(u1a)
    print(u1b)
    print('===============================')

    '''---Initialize Metric---'''
    #metric1 = np.zeros((len(cname1), len(cname2)))
    #metric2 = np.zeros((len(cname1), len(cname2)))
    metric = np.zeros((len(cname1), len(cname2)))
    print('===============================')
    print("metric")
    print(metric)
    print(metric.shape)
    print('===============================')

    '''---Map the value---'''
    indtmp = np.ravel_multi_index((u2a, u2b), metric.shape)
    print('===============================')
    print("indtmp")
    print(indtmp)
    print(indtmp.shape)
    print("===============================")

    #tmpk1 = info[:, 2]
    #tmpk2 = info[:, 3]
    tmpk = info[:, 4]
    print('===============================')
    print("tmpk")
    print(tmpk)
    print(tmpk.shape)
    print('===============================')
    #metric1.flat[indtmp] = tmpk1
    #metric2.flat[indtmp] = tmpk2
    metric.flat[indtmp] = tmpk
    print('===============================')
    print("metric")
    print(metric)
    print('===============================')

    '''---metric_origin---'''
    scaled_data_origin = (metric -metric.min()) / (metric.max() - metric.min()) * 100  # to percentage
    metric_origin_percentage_df = pd.DataFrame(scaled_data_origin, index=cname1, columns=cname2)  # 將索引設置為 cname1 和 cname2
    print('===============================')
    print("metric3n_normalzie")
    print(metric_origin_percentage_df.head(5))
    print('===============================')

    '''---metric_normalize---'''
    scaler = StandardScaler()
    normalized_data = scaler.fit_transform(metric)
    #scaled_data = normalized_data*10+50
    scaled_data = (normalized_data - normalized_data.min()) / (normalized_data.max() - normalized_data.min()) * 100  # to percentage
    metric_normalize_percentage_df = pd.DataFrame(scaled_data, index=cname1, columns=cname2)  # 將索引設置為 cname1 和 cname2
    print('===============================')
    print("metric_normalzie_df")
    print(metric_normalize_percentage_df.head(5))
    print('===============================')

    '''---metric_log---'''
    metric_log = np.log(metric+1)
    metric_log_df = pd.DataFrame(metric_log, index=cname1, columns=cname2)
    print('===============================')
    print("metric_log_df")
    print(metric_log_df.head(5))
    print('===============================')

    '''---metric_log_percentage---'''
    normalized_log_data = scaler.fit_transform(metric_log)
    scaled_data_log = (normalized_log_data - normalized_log_data.min()) / (normalized_log_data.max() - normalized_log_data.min()) * 100  # to percentage
    metric_log_percentage_df = pd.DataFrame(scaled_data_log,index=cname1, columns=cname2)
    print('===============================')
    print("metric_log_percentage_df")
    print(metric_log_percentage_df.head(5))
    print('===============================')
    
    '''Choose graph type'''
    metric = [metric_origin_percentage_df ,metric_normalize_percentage_df,metric_log_df,metric_log_percentage_df]
    normalize = [True,False]
    save_dir_selection = ['images/clustermap_origin_percentage.png','images/clustermap_normalize_percentage.png', 'images/clustermap_log.png','images/clustermap_log_percentage.png']

    print("What type of information do you want in your plot? Choose 0,1 o 2 depending on the awnser")
    print('Original metrics, Normalized percentages or Logarithm of percentages')
    ch1 = int(input('Input selection: '))
    print("")

    print("Do you wnat to normalize the data? Choose 0 or 1 depending on the awnser")
    print('True, False')
    ch2 = int(input('Input selection: '))
    print("")

    print("What name do you want to give your plot?  Do NOT write the file type (e.g., png, jpeg, etc)")
    ch3 = input('Write name (do not leave spaces): ')
    print("")
    
    save_dir_selection = f'images/{ch3}.png'
    plot_clustermap(metric[ch1],normalize[ch2],save_dir_selection)

    from  PIL import Image

    img = Image.open(save_dir_selection)
    img.show()


if __name__ == "__main__":
    datafd = input('Data folder URL?\n')
    datafd = datafd.replace('\\', '/')
    main(datafd)
    