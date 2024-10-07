import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures, StandardScaler, OneHotEncoder
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor



merged_df = pd.read_csv('./db/model.csv')

# Assuming df is your DataFrame
X = merged_df[['year', 'km_driven', 'fuel', 'seller_type', 'transmission', 'mileage', 'engine', 'max_power', 'seats']]
y = merged_df['selling_price']

# Encode categorical variables
encoder = OneHotEncoder()
X_encoded = encoder.fit_transform(X[['fuel', 'seller_type', 'transmission']]).toarray()

# Combine encoded features with numerical features
X_numerical = X[['year', 'km_driven', 'mileage', 'engine', 'max_power', 'seats']].values
X_combined = np.hstack((X_numerical, X_encoded))

# Polynomial features
poly = PolynomialFeatures(degree=2, interaction_only=True)
X_poly = poly.fit_transform(X_combined)

# Log transformation
X_log = np.log(X_combined + 1)  # Adding 1 to avoid log(0)

# Standardization
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_combined)

# PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_combined)


# After training your model and fitting your transformers
pickle.dump(encoder, open('encoder.pkl','wb'))
pickle.dump(poly, open('poly.pkl','wb'))
pickle.dump(scaler, open('scaler.pkl','wb'))
pickle.dump(pca, open('pca.pkl','wb'))

# Combine all features
X_final = np.hstack((X_combined, X_poly, X_log, X_scaled, X_pca))

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X_final, y, test_size=0.2, random_state=42)

# Train a Random Forest model
rf = RandomForestRegressor(random_state=42)
rf.fit(X_train, y_train)


pickle.dump(rf,open('model.pkl','wb')) #Write binary mode - wb

print("Model built.")
# predictions = model.predict(X_test)

# # Calculate metrics
# mae = mean_absolute_error(y_test, predictions)
# mse = mean_squared_error(y_test, predictions)
# rmse = mean_squared_error(y_test, predictions, squared=False)
# r2 = r2_score(y_test, predictions)
# mape = np.mean(np.abs((y_test - predictions) / y_test)) * 100

# Display metrics
# print("MAE:", mae)
# print("MSE:", mse)
# print("RMSE:", rmse)
# print("R²:", r2)
# print("MAPE:", mape)

# # # Create a DataFrame to compare actual and predicted values
# # comparison_df = pd.DataFrame({'Actual': y_test, 'Predicted': predictions})
# # # print(comparison_df.head())

# # Create a DataFrame to compare actual and predicted values
# comparison_df = pd.DataFrame({'Actual': y_test, 'Predicted': predictions})
# print(comparison_df.head())
