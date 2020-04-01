#compare_type为-1，则表示小于；为0，则表示等于；为1，则表示大于
def count_within_period(stock_data_column,current_index,input_para,period,compare_type):
    appreance_times = 0#计数器
    boundary_index = current_index - period + 1

    for index in range(boundary_index,current_index+1):
        if compare_type == 1:
            if stock_data_column[index] > input_para:
                appreance_times += 1
        elif compare_type == -1:
            if stock_data_column[index] < input_para:
                appreance_times += 1
        else:
            # print(input_para)
            # print(stock_data_column[index])
            # print("-----------------------")
            if abs((stock_data_column[index] - input_para)) < 1e-5:
                appreance_times += 1
    return appreance_times