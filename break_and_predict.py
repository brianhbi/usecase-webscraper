import fasttext
import re
import heapq

def get_clean_model_dict(prediction, threshold):

    labels = list(prediction[0])
    probs = list(prediction[-1])

    translation = {'machineconditionmonitoring': 'Machine Condition Monitoring',
                    'logisassetmanagement': 'Logistics & Asset Management',
                    'infoperationcontrol': 'Infrastructure & Operations Control Optimization',
                    'interactivedisplays': 'Interactive Displays',
                    'securitysurveillance': 'Security & Surveillance',
                    'energymanagement': 'Energy Management',
                    'outdoormonitoring': 'Outdoor Environmental Monitoring',
                    'indoormonitoring': 'Indoor Environmental Monitoring',
                    'healthwellness': 'Health & Wellness',
                    'autonomousnavigation': 'Autonomous Navigation'}
    dict = {}
    for i in range(len(labels)):
        clean_label = labels[i].replace('__label__', '')
        labels[i] = translation.get(clean_label)
        if probs[i] >= threshold: # exclude labels below threshold
            dict.update( { labels[i] : probs[i] } )

    return dict

def group_words(s, n):
    words = s.split()
    for i in range(0, len(words), n):
        yield ' '.join(words[i:i+n])

def split_file_into_chunks(text, chunk_size, model):
    print("\nPrediction of whole text together:", model.predict(text.strip(), k=3))
    all_chunks = list(group_words(text, chunk_size))
    # print(all_chunks)
    return all_chunks

def predict(text, modelname, threshold):
    model = fasttext.load_model(modelname) # train_model(param)

    keys = {'Machine Condition Monitoring', 'Logistics & Asset Management',
            'Infrastructure & Operations Control Optimization',
            'Interactive Displays', 'Security & Surveillance',
            'Energy Management', 'Outdoor Environmental Monitoring',
            'Indoor Environmental Monitoring', 'Health & Wellness',
            'Autonomous Navigation'}

    chunks = split_file_into_chunks(text, 50, model)
    # print(len(chunks))

    if len(chunks) > 2: # if text is less than 200 words, don't bother breaking up
        all_predictions = {key: [] for key in keys} # {"S&S": [P(chunk_1), ..., P(chunk_n)], ..., "EnMgmt": [P(chunk_1), ..., P(chunk_n)]}

        for chunk in chunks:
            prediction = model.predict(chunk.strip(), k=-1)
            clean_prediction_dict = get_clean_model_dict(prediction, 0) # {"S&S": P(chunk_i), ..., "EnMgmt": P(chunk_i)}

            for key in clean_prediction_dict:
                chunk_prob = clean_prediction_dict[key]
                all_predictions[key].append(chunk_prob) # add to the bigger dict

        final_model_dict = {}
        for key in keys:
            probs_list = all_predictions[key]
            n = int(len(chunks) / 4) # take the n highest probabilities
            n_largest = heapq.nlargest(n, probs_list)
            # print("key:", key, "n largest:", n_largest)
            new_prob = sum(n_largest) / len(n_largest)
            if new_prob >= threshold:
                final_model_dict[key] = new_prob
        return sorted(final_model_dict.items(), key = lambda x : x[1], reverse=True) # sorted dict

    else:
        prediction = model.predict(text.strip(), k=-1)
        return get_clean_model_dict(prediction, threshold)

file = open("test-hisec.txt", 'r')
text = file.read()

prediction = predict(text, "model_100_400_0.1_2_ova.bin", 0.2)
print(prediction)
