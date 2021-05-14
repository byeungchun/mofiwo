import os
import pickle
import tensorflow as tf

from concurrent import futures
from tensorflow import keras
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from skopt import BayesSearchCV
from skopt.space import Real, Categorical, Integer

def generate_bayes_optimized_randomforest(train_data):
    X_train = train_data[0]['x_train']
    y_train = train_data[0]['y_train']

    search_space = {"bootstrap": Categorical([True, False]), # values for boostrap can be either True or False
            "max_depth": Integer(6, 20), # values of max_depth are integers from 6 to 20
            "max_features": Categorical(['auto', 'sqrt','log2']), 
            "min_samples_leaf": Integer(2, 10),
            "min_samples_split": Integer(2, 10),
            "n_estimators": Integer(100, 500)
        }

    forest_clf = RandomForestClassifier()

    best_scores = list()
    def on_step(optim_result):
        if forest_bayes_search.best_score_ >= 0.90:
            print('Interrupting!')
            return True
        else:
            best_scores.append([forest_bayes_search.best_index_, forest_bayes_search.best_score_])
        if len(best_scores) % 5 == 0:
            print(f'# of exercises: {len(best_scores):5}(score: {round(forest_bayes_search.best_score_,3)})')

    forest_bayes_search = BayesSearchCV(forest_clf, search_space, n_iter=32, scoring="accuracy", n_jobs=-1, cv=5)
    forest_bayes_search.fit(X_train, y_train, callback=on_step)
    
    return forest_bayes_search   

def execute_random_forest(train_data, model_folder, model_name):

    with futures.ProcessPoolExecutor(max_workers=3) as executor:
        for _input, _result in zip(train_data, executor.map(generate_bayes_optimized_randomforest, train_data)):
            save_ml_model(_input[0], _result, model_folder, model_name)

def save_ml_model(_input, ml_model, model_folder, model_name):
    
    dump = {
        'ml_model':ml_model,
        'test_seq':_input['feature_test_id'],
        'x_test':_input['x_test'],
        'y_test':_input['y_test'],
        'features':_input['features']
    }
    pickle.dump(dump, open(os.path.join(os.path.expanduser(model_folder),f'{model_name}_{_input["_id"]:03d}.pickle'), 'wb'))
