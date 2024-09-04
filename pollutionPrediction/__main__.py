import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression

# Generate synthetic air quality data
data = pd.DataFrame({
    'temperature': np.random.uniform(15, 35, 1000),
    'humidity': np.random.uniform(30, 90, 1000),
    'CO': np.random.uniform(0.1, 1.0, 1000),  # Carbon Monoxide levels
    'NO2': np.random.uniform(10, 60, 1000),  # Nitrogen Dioxide levels
    'PM10': np.random.uniform(20, 100, 1000),  # Particulate Matter 10
    'AQI': np.random.uniform(50, 300, 1000)  # Air Quality Index
})

# Separate features and target variable
X = data[['temperature', 'humidity', 'CO', 'NO2', 'PM10']]
y = data['AQI']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Initialize and train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse:.2f}')
print(f'R^2 Score: {r2:.2f}')

# Example prediction
new_data = np.array([[30, 65, 0.5, 40, 70]])  # Sample new data input
new_data_scaled = scaler.transform(new_data)
predicted_aqi = model.predict(new_data_scaled)

print(f'Predicted AQI: {predicted_aqi[0]:.2f}')
