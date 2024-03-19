import scripts.variables

def load_config():
    file_path = 'config/config.txt'
    words = []
    
    # loading and reading the 'config.txt' file, then adding each word to array
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line_words = line.strip()
                words.append(line_words)
        
        # darkmode
        if words[1] == 'yes':
            darkmode = True
        else:
            darkmode = False
    
        # geometry
        geometry = f'{words[3]}x{words[5]}'
    
        # language
        scripts.variables.LANGUAGE = words[7]

        return words, darkmode, geometry
                    
    except FileNotFoundError:
        print('The file "config.txt" is missing!')
        
