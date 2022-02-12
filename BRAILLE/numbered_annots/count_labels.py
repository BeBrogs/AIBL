import subprocess as sp


def get_listing():
    files_bytes = sp.check_output("ls", shell=True)
    files_str = files_bytes.decode('utf-8')
    listing = files_str.split('\n')
    return listing


def get_xml_file_names(listing_arr):
    xml_files = []
    for file in listing_arr:
        if file[-4:] == '.xml':
            xml_files.append(file)

    return xml_files


def count_labels_in_all_files(xml_files):
    label_dict = {}
    print(xml_files[0])

    for file in xml_files:
        with open(file, 'r') as f:
            for line in f:
                if '<name>' in line:
                    name_formatted = line.split('>')[1].split('<')[0]
                    if name_formatted in label_dict.keys():
                        label_dict[name_formatted] += 1
                    else:
                        label_dict[name_formatted] = 0

    avg = 0
    
    for i, j in label_dict.items():
        print(i, j)
        avg += int(j)

    print(avg/26)


if __name__ == '__main__':
    listing_arr = get_listing()
    xml_files = get_xml_file_names(listing_arr)
    count_labels_in_all_files(xml_files)


