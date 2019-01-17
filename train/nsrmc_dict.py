# -*- coding:utf-8 -*-
import collections

if __name__ == "__main__":

    # path = './'
    #
    # file_name = path + '1928101.txt'
    #
    # name_set = set()
    #
    # with open(file_name, 'r') as f:
    #     lines = f.readlines()
    #
    #     for i in lines:
    #         ll = i.strip()
    #         name_set = name_set | set(ll)
    #
    # name_list = list(name_set)
    # list2 = list(range(1, len(name_list)+1))
    #
    # name_dict = dict(zip(name_list, list2))
    # print(name_dict)
    #
    # with open('./nsrmc_chn.txt', 'w') as f2:
    #     res = []
    #     res.append('\n')
    #     for i in name_list:
    #         temp = i + '\n'
    #         res.append(temp)
    #
    #     f2.writelines(res)


    file_name = './nsrmc_chn.txt'

    name_dict = {}

    with open(file_name, 'r') as f:
        lines = f.readlines()
        index = 0

        for i in lines:
            temp_key = i.replace('\n', '')
            name_dict[temp_key] = index
            index += 1







    # path = './label_test.txt'
    #
    # with open(path, 'r') as f1:
    #     res = []
    #     lines = f1.readlines()
    #     for i in lines:
    #         ll = i.strip().split(' ')
    #
    #         temp_list = list(ll[1])
    #         for i in range(len(temp_list)):
    #             temp_list[i] = str(name_dict[temp_list[i]])
    #
    #         ll[1] = ' '.join(temp_list)
    #         temp_str = str(ll[0]) + ' ' + str(ll[1]) + '\n'
    #         print(temp_str)
    #         res.append(temp_str)
    #
    # with open('./nsrmc_test1.txt', 'w') as f2:
    #     f2.writelines(res)


    with open('./nsrmc_train_34W.txt', 'r') as f1:
        res = []
        lines = f1.readlines()
        for i in lines:
            ll = i.strip().split(' ')

            temp_list = list(ll[1])
            for i in range(len(temp_list)):
                temp_list[i] = str(name_dict[temp_list[i]])

            ll[1] = ' '.join(temp_list)
            temp_str = str(ll[0]) + '.jpg' + ' ' + str(ll[1]) + '\n'
            print(temp_str)
            res.append(temp_str)

    with open('./nsrmc_train_34_1.txt', 'w') as f2:
        f2.writelines(res)



