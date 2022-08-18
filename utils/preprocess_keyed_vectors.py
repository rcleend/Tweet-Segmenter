class PreprocessKeyedVectors:
    def __init__(self):
        print('Preprocessing file')
        with open('../data/enwiki_titles.txt', 'w') as title_file:
            with open('../data/enwiki_keyed_vectors.txt', 'w') as vector_file:
                with open('../data/enwiki_20180420_100d.txt') as old_file:
                    lines = old_file.readlines()
                    i = 0
                    for line in lines:
                        if line.startswith('ENTITY'):
                            title = line.split()[0]
                            vector_file.write(line)
                            title_file.write(title + '\n')

                        if i > 5000: break

                        i += 1

                old_file.close()
            vector_file.close()
        title_file.close()
        print('Finished preprocessing file')


if __name__ == '__main__':
    preprocessor = PreprocessKeyedVectors()
