def check_if_file_valid(filename):
    '''
    Function to check validity of Assignment 4 output file
    Input: the output filename ('output4.txt')
    Output: Returns validity statement
    '''
    assert filename == 'output4.txt', 'Incorrect filename'
    f = open(filename).read()
    l = f.split('\n')
    assert len(l) == 5000, 'Incorrect number of items'
    assert (len(set(l)) == 1 or len(set(l)) == 2), 'Wrong class labels'
    
    return 'The output file is valid'

FILENAME = 'output4.txt'
print(check_if_file_valid(FILENAME))