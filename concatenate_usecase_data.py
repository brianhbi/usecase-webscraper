import shutil
import os

def main():
    curr_file_dir = os.path.dirname(os.path.realpath('__file__'))
    join_dir = os.path.join(curr_file_dir, 'usecase_data/')
    os.chdir(join_dir)

    with open('train_final_all.txt','wb') as wfd:
        for f in ['train_machineconditionmonitoring.txt',
                  'train_logisticstracking.txt',
                  'train_assetoperationsoptimization.txt',
                  'train_interactivedisplays.txt',
                  'train_situationalsurveillance.txt',
                  'train_energymonitoringmanagement.txt',
                  'train_environmentmonitoring.txt',
                  'train_controloptimizationautonomy.txt',
                  'train_humanwellnessmonitoring.txt',
                  'train_productinspection.txt']:
            with open(f,'rb') as fd:
                shutil.copyfileobj(fd, wfd) #concatenates all training data
    with open('test_final_all.txt','wb') as wdf:
        for g in ['test_machineconditionmonitoring.txt',
                  'test_logisticstracking.txt',
                  'test_assetoperationsoptimization.txt',
                  'test_interactivedisplays.txt',
                  'test_situationalsurveillance.txt',
                  'test_energymonitoringmanagement.txt',
                  'test_environmentmonitoring.txt',
                  'test_controloptimizationautonomy.txt',
                  'test_humanwellnessmonitoring.txt',
                  'test_productinspection.txt']:
            with open(g,'rb') as gf:
                shutil.copyfileobj(gf, wdf) #concatenates all testing data

if __name__ == "__main__":
    main()
