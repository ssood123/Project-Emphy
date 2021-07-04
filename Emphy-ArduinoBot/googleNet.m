%% Initialization
clear
clc
typeofnet = 'googlenet';
net = googlenet();
trainingSet = imageDatastore({'C:\Users\Owner\Desktop\importantImages\Chair','C:\Users\Owner\Desktop\importantImages\Desk','C:\Users\Owner\Desktop\importantImages\Shoe'},'LabelSource','foldernames');

%% training

for i = 1:2
    imageSize = net.Layers(1).InputSize;
    augmentedTrainingSet = augmentedImageDatastore(imageSize, trainingSet, 'ColorPreprocessing', 'gray2rgb');
    

    featureLayer = 'pool5-7x7_s1';
  
    
    
    trainingFeatures = activations(net, augmentedTrainingSet, featureLayer, 'MiniBatchSize', 32, 'OutputAs', 'columns');
    
    trainingLabels = trainingSet.Labels;
    classifier = fitcecoc(trainingFeatures, trainingLabels, 'Learner', 'Linear', 'Coding', 'onevsall', 'ObservationsIn', 'columns');
end