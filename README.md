Run create_dataset_for_use_case.py to create use case data for a SPECIFIC use case category.
Eg. "python create_dataset_for_use_case.py interactivedisplays"

After creating the dataset for each use case, run concatenate_usecase_data.py to combine ALL use case data into two files for training and testing.
Eg. "python concatenate_usecase_data.py"

Then you're free to use Fasttext to train a text classifier model.
