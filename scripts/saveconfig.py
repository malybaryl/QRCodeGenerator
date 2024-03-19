def save_config(words):
    file_path = 'config/config.txt'

    try:
        with open(file_path, 'w') as file:
            # writing words to config file
            for word in words:
                file.write(word + '\n')
                
    except Exception as e:
        print('An error occurred while writing to the file:', e)