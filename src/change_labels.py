import os

class_mapping = {
    'common myna': 0,
    'grey crow': 1,
    'pigeon': 2
}

base_dir = 'Dataset/'

for bird_species, class_id in class_mapping.items():
    
    for dataset_type in ['train', 'valid', 'test']:
        label_dir = os.path.join(base_dir, bird_species, dataset_type, 'labels')

        for label_file in os.listdir(label_dir):
            if label_file.endswith('.txt'):
                label_path = os.path.join(label_dir, label_file)

                with open(label_path, 'r') as f:
                    lines = f.readlines()

                # Update the class ID for each line in the file
                updated_lines = []
                for line in lines:
                    parts = line.strip().split(' ')
                    parts[0] = str(class_id) 
                    updated_line = ' '.join(parts)
                    updated_lines.append(updated_line)

                with open(label_path, 'w') as f:
                    f.write('\n'.join(updated_lines))

    print(f"Updated labels for {bird_species} with class ID {class_id}")