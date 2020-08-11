from utils_mariadb import select_data_evac, save_data_to_sql_file


data = select_data_evac()
save_data_to_sql_file(data)