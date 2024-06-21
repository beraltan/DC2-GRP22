import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


def load_data(file_path, features, target):
    """
    Load the dataset from a CSV file.

    Parameters:
    - file_path: str, path to the CSV file.
    - features: list of str, the feature column names.
    - target: str, the target column name.

    Returns:
    - X: DataFrame, features.
    - y: Series, target.
    """
    data = pd.read_csv(file_path)
    X = data[features]
    y = data[target]
    return X, y


def train_xgboost(X, y, test_size=0.2, random_state=42, num_boost_round=100):
    """
    Train an XGBoost model.

    Parameters:
    - X: DataFrame, features.
    - y: Series, target.
    - test_size: float, proportion of the dataset to include in the test split.
    - random_state: int, random state for train_test_split.
    - num_boost_round: int, number of boosting rounds.

    Returns:
    - bst: trained XGBoost model.
    - feature_names: list of str, feature names.
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dtest = xgb.DMatrix(X_test, label=y_test)

    params = {
        'objective': 'multi:softprob',
        'num_class': len(y.unique()),
        'eval_metric': 'mlogloss'
    }

    bst = xgb.train(params, dtrain, num_boost_round=num_boost_round)

    return bst, X.columns


def plot_feature_importance(bst, feature_names):
    """
    Plot feature importance.

    Parameters:
    - bst: trained XGBoost model.
    - feature_names: list of str, feature names.
    """
    importance = bst.get_score(importance_type='weight')
    importance_df = pd.DataFrame({
        'Feature': [feature_names[int(k[1:])] for k in importance.keys()],
        'Importance': importance.values()
    }).sort_values(by='Importance', ascending=False)

    plt.figure(figsize=(10, 6))
    plt.barh(importance_df['Feature'], importance_df['Importance'])
    plt.xlabel('Importance')
    plt.ylabel('Feature')
    plt.title('Feature Importance from XGBoost Model')
    plt.gca().invert_yaxis()
    plt.show()

    return importance_df


# Example usage
file_path = '../qwe/everythingMerged.csv'  # Replace with your file path
features = ['SubjectAge', 'Tactic 1', 'PrimaryConduct', 'SubjectInjured', 'MainDuty',
    'Outcome: Made off/escaped', 'Outcome: Arrested', 'Outcome: Hospitalised',
    'Outcome: Detained - Mental Health Act', 'Outcome: Fatality', 'Outcome: Other']  # Replace with your feature columns
target = 'Average Score'  # Replace with your target column

# Load data
X, y = load_data(file_path, features, target)

# Train model
bst, feature_names = train_xgboost(X, y)

# Plot feature importance
importance_df = plot_feature_importance(bst, feature_names)
importance_df