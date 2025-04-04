
# Kategorik verileri dönüştür
X_encoded = pd.get_dummies(X)

# Label encode target (product_id)
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Eğitim ve test bölme
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y_encoded, test_size=0.2, random_state=42)

# Ölçekleme
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

"""# XGBoost Modeli
xgb_model = xgb.XGBClassifier(eval_metric='logloss')#0.99
xgb_model.fit(X_train, y_train)
y_pred_xgb = xgb_model.predict(X_test)"""

# Random Forest Modeli
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)#0.5
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)
""""
# Gradient Boosting Modeli
gb_model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, random_state=42)#0.9
gb_model.fit(X_train, y_train)
y_pred_gb = gb_model.predict(X_test)"""

# Model Performansı
def evaluate_model(y_test, y_pred, model_name):#0.03
    acc = accuracy_score(y_test, y_pred)
    print(f"{model_name} Performansı:")
    print(f"Doğruluk (Accuracy): {acc:.4f}")
    print(classification_report(y_test, y_pred))
    print("-" * 30)

#evaluate_model(y_test, y_pred_xgb, "XGBoost")
evaluate_model(y_test, y_pred_rf, "Random Forest")
#evaluate_model(y_test, y_pred_gb, "Gradient Boosting")
"""
# Ensemble Voting (basit oylama)
y_pred_ensemble = (y_pred_xgb + y_pred_rf + y_pred_gb)
y_pred_ensemble = (y_pred_ensemble >= 2).astype(int)  # 3 modelden en az 2'si aynı sınıfı diyorsa
evaluate_model(y_test, y_pred_ensemble, "Ensemble (XGBoost + RF + GB)")

# Stacking Ensemble
estimators = [
    ('xgb', xgb_model),
    ('rf', rf_model),
    ('gb', gb_model)
]
stacking_model = StackingClassifier(estimators=estimators, final_estimator=LogisticRegression(), cv=5)
stacking_model.fit(X_train, y_train)
y_pred_stacking = stacking_model.predict(X_test)
evaluate_model(y_test, y_pred_stacking, "Stacking Model")
"""
# Modelleri Kaydet
with open("stacking_model.pkl", "wb") as model_file:
    pickle.dump(rf_model, model_file)

with open("scaler.pkl", "wb") as scaler_file:
    pickle.dump(scaler, scaler_file)

# LabelEncoder'ı da kaydet (opsiyonel ama önerilir)
with open("label_encoder.pkl", "wb") as le_file:
    pickle.dump(le, le_file)

print("Modeller başarıyla kaydedildi!")

# Kaydedilen modeli yükleme (test için)
with open("stacking_model.pkl", "rb") as model_file:
    loaded_model = pickle.load(model_file)

with open("scaler.pkl", "rb") as scaler_file:
    loaded_scaler = pickle.load(scaler_file)

"""import matplotlib.pyplot as plt
import xgboost as xgb

# Modeli XGBoost ile eğitirken eval_metric ve eval_set ekleyelim
evals = [(X_train, y_train), (X_test, y_test)]  # Eğitim ve test verilerini kullanarak

xgb_model = xgb.XGBClassifier(eval_metric=['logloss', 'error'])  # Kayıp (logloss) ve hata (error) takibi

# Modeli eğitirken, her iterasyonda metrikleri kaydet
history = xgb_model.fit(X_train, y_train, 
                        eval_set=evals, 
                        verbose=True)  # Eğitim sırasında metriklerin çıktısını al

# Eğitim sonrası doğruluk ve kayıp metriklerini çekelim
eval_results = history.evals_result()

# Doğruluk ve Kayıp Grafiklerini Çizme
plt.figure(figsize=(12, 6))

# Kayıp Grafiği (logloss)
plt.subplot(1, 2, 1)
plt.plot(eval_results['validation_0']['logloss'], label='Train Log Loss')
plt.plot(eval_results['validation_1']['logloss'], label='Test Log Loss')
plt.title('Log Loss Over Training Iterations')
plt.xlabel('Iterations')
plt.ylabel('Log Loss')
plt.legend()

# Doğruluk Grafiği (error)
plt.subplot(1, 2, 2)
plt.plot(eval_results['validation_0']['error'], label='Train Accuracy')
plt.plot(eval_results['validation_1']['error'], label='Test Accuracy')
plt.title('Error Rate Over Training Iterations')
plt.xlabel('Iterations')
plt.ylabel('Error Rate')
plt.legend()

plt.tight_layout()
plt.show()
"""