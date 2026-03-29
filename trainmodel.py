import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import LabelEncoder
import pickle

df = pd.read_csv("miami_rentals.csv")
df.dropna(subset=["price", "sqft", "beds", "baths", "year_built"], inplace=True)

# remove outliers — anything above $10k/mo is skewing the model
df = df[df["price"] < 10000]

le = LabelEncoder()
df["property_type_enc"] = le.fit_transform(df["property_type"])

features = ["beds", "baths", "sqft", "year_built", "zip", "property_type_enc"]
X = df[features]
y = df["price"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = GradientBoostingRegressor(n_estimators=500, max_depth=5, learning_rate=0.05, random_state=42)
model.fit(X_train, y_train)

preds = model.predict(X_test)
mae = mean_absolute_error(y_test, preds)
print(f"Mean Absolute Error: ${mae:.0f}")

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
with open("encoder.pkl", "wb") as f:
    pickle.dump(le, f)

print("Model saved.")