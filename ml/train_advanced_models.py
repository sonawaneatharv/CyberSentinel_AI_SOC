"""
Advanced ML Model Training Pipeline
Trains:
1. Stage 1 Binary Gatekeeper: Benchmark comparison of LightGBM, XGBoost, Random Forest, Decision Tree
2. Stage 2 Multi-Class Classifier: LightGBM / XGBoost for known threats (DoS, PortScan, BruteForce, Botnet)
3. Stage 3 Unsupervised Zero-Day Anomaly Engine: Isolation Forest calibrated on Benign baseline flows
4. Explainable AI (XAI): SHAP TreeExplainer integration for real-time feature attribution
5. Exports metrics_summary.json with full viva tables and MITRE mappings
"""

import os
import json
import time
import numpy as np
import joblib

# Scikit-Learn metrics & baseline models
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# Advanced Gradient Boosters
import lightgbm as lgb
import xgboost as xgb
import shap

BASE_DIR = os.path.dirname(__file__)
PROCESSED_DIR = os.path.join(BASE_DIR, "..", "data", "processed")
MODELS_DIR = os.path.join(BASE_DIR, "models")

MITRE_MAPPINGS = {
    "DoS": {
        "technique_id": "T1498",
        "technique_name": "Network Denial of Service",
        "tactic": "Impact",
        "cvss": 7.5,
        "severity": "HIGH",
        "description": "Adversary performs volumetric or state-exhaustion flooding against critical service ports."
    },
    "PortScan": {
        "technique_id": "T1046",
        "technique_name": "Network Service Discovery",
        "tactic": "Reconnaissance",
        "cvss": 5.3,
        "severity": "MEDIUM",
        "description": "Adversary probes ranges of ports to map open listening services and potential entry points."
    },
    "BruteForce": {
        "technique_id": "T1110",
        "technique_name": "Brute Force",
        "tactic": "Credential Access",
        "cvss": 8.1,
        "severity": "HIGH",
        "description": "Adversary repeatedly attempts authentication credential combinations across SSH/FTP endpoints."
    },
    "Botnet": {
        "technique_id": "T1071",
        "technique_name": "Application Layer Protocol: C2",
        "tactic": "Command and Control",
        "cvss": 8.8,
        "severity": "CRITICAL",
        "description": "Infected zombie host maintains periodic beacon communication with remote command servers."
    },
    "ZeroDay_Anomaly": {
        "technique_id": "T1203",
        "technique_name": "Exploitation for Client Execution",
        "tactic": "Initial Access / Unknown",
        "cvss": 9.4,
        "severity": "CRITICAL",
        "description": "Unsupervised telemetry engine detected an anomalous flow with extreme reconstruction variance."
    }
}

def load_data():
    X_train = np.load(os.path.join(PROCESSED_DIR, "X_train_scaled.npy"))
    X_test = np.load(os.path.join(PROCESSED_DIR, "X_test_scaled.npy"))
    y_bin_train = np.load(os.path.join(PROCESSED_DIR, "y_bin_train.npy"))
    y_bin_test = np.load(os.path.join(PROCESSED_DIR, "y_bin_test.npy"))
    y_mul_train = np.load(os.path.join(PROCESSED_DIR, "y_mul_train.npy"), allow_pickle=True)
    y_mul_test = np.load(os.path.join(PROCESSED_DIR, "y_mul_test.npy"), allow_pickle=True)

    with open(os.path.join(MODELS_DIR, "selected_features.json")) as f:
        features = json.load(f)

    return X_train, X_test, y_bin_train, y_bin_test, y_mul_train, y_mul_test, features

def train_and_export():
    print("[*] Loading preprocessed arrays...")
    X_train, X_test, y_bin_train, y_bin_test, y_mul_train, y_mul_test, features = load_data()

    # -------------------------------------------------------------
    # 1. STAGE 1: BENCHMARK COMPARISON EXPERIMENT
    # -------------------------------------------------------------
    print("\n" + "="*70)
    print("STEP 1: Model Benchmark Comparison (Binary Threat Gatekeeper)")
    print("="*70)

    candidate_models = {
        "LightGBM": lgb.LGBMClassifier(n_estimators=100, learning_rate=0.08, num_leaves=31, random_state=42, verbose=-1),
        "XGBoost": xgb.XGBClassifier(n_estimators=100, learning_rate=0.08, max_depth=6, random_state=42, eval_metric="logloss"),
        "Random Forest": RandomForestClassifier(n_estimators=60, max_depth=12, random_state=42, n_jobs=-1),
        "Decision Tree": DecisionTreeClassifier(max_depth=10, random_state=42)
    }

    comparison_results = []
    best_binary_model = None
    best_f1 = -1.0
    best_model_name = ""

    for name, clf in candidate_models.items():
        t0 = time.time()
        clf.fit(X_train, y_bin_train)
        train_time = round(time.time() - t0, 3)

        t1 = time.time()
        y_pred = clf.predict(X_test)
        infer_latency_ms = round(((time.time() - t1) / len(X_test)) * 1000, 4)

        acc = float(accuracy_score(y_bin_test, y_pred))
        prec = float(precision_score(y_bin_test, y_pred, zero_division=0))
        rec = float(recall_score(y_bin_test, y_pred, zero_division=0))
        f1 = float(f1_score(y_bin_test, y_pred, zero_division=0))
        cm = confusion_matrix(y_bin_test, y_pred).tolist()

        res = {
            "model_name": name,
            "accuracy": round(acc * 100, 2),
            "precision": round(prec * 100, 2),
            "recall": round(rec * 100, 2),
            "f1_score": round(f1 * 100, 2),
            "train_time_sec": train_time,
            "latency_ms_per_flow": infer_latency_ms,
            "confusion_matrix": cm
        }
        comparison_results.append(res)
        print(f"[{name:15}] Acc: {res['accuracy']:6.2f}% | Recall: {res['recall']:6.2f}% | F1: {res['f1_score']:6.2f}% | Latency: {infer_latency_ms} ms")

        # Pick LightGBM or highest F1
        if f1 > best_f1:
            best_f1 = f1
            best_binary_model = clf
            best_model_name = name

    print(f"\n[+] Selected Champion Binary Classifier: {best_model_name} (F1: {round(best_f1*100, 2)}%)")
    joblib.dump(best_binary_model, os.path.join(MODELS_DIR, "binary_model.joblib"))

    # Feature Importance for Stage 1
    feature_importances = []
    if hasattr(best_binary_model, "feature_importances_"):
        imps = best_binary_model.feature_importances_
        # Normalize to percentage
        total_imp = np.sum(imps)
        norm_imps = (imps / total_imp) * 100 if total_imp > 0 else imps
        sorted_indices = np.argsort(norm_imps)[::-1]
        for idx in sorted_indices:
            feature_importances.append({
                "feature": features[idx],
                "importance": round(float(norm_imps[idx]), 2)
            })

    # -------------------------------------------------------------
    # 2. STAGE 2: MULTI-CLASS ATTACK CLASSIFIER (LightGBM)
    # -------------------------------------------------------------
    print("\n" + "="*70)
    print("STEP 2: Stage 2 Multi-Class Classifier (Specialized Attack Category)")
    print("="*70)

    attack_mask_train = (y_mul_train != "BENIGN")
    attack_mask_test = (y_mul_test != "BENIGN")

    X_att_train = X_train[attack_mask_train]
    y_att_train = y_mul_train[attack_mask_train]
    X_att_test = X_test[attack_mask_test]
    y_att_test = y_mul_test[attack_mask_test]

    attack_classes = sorted(list(set(y_att_train)))
    print(f"[*] Training multi-class classifier on threats: {attack_classes}")

    # Use LightGBM for ultra-fast multi-class classification
    multiclass_clf = lgb.LGBMClassifier(
        n_estimators=80,
        learning_rate=0.08,
        num_leaves=31,
        random_state=42,
        verbose=-1
    )
    multiclass_clf.fit(X_att_train, y_att_train)

    y_att_pred = multiclass_clf.predict(X_att_test)
    multi_acc = float(accuracy_score(y_att_test, y_att_pred))
    multi_cm = confusion_matrix(y_att_test, y_att_pred, labels=attack_classes).tolist()
    rep = classification_report(y_att_test, y_att_pred, output_dict=True)

    print(f"[+] Stage 2 Multi-Class Accuracy: {round(multi_acc * 100, 2)}%")
    joblib.dump(multiclass_clf, os.path.join(MODELS_DIR, "multiclass_model.joblib"))

    # -------------------------------------------------------------
    # 3. STAGE 3: UNSUPERVISED ZERO-DAY ANOMALY DETECTOR
    # -------------------------------------------------------------
    print("\n" + "="*70)
    print("STEP 3: Training Unsupervised Zero-Day Anomaly Engine")
    print("="*70)
    # Train Isolation Forest purely on BENIGN baseline traffic
    benign_mask_train = (y_mul_train == "BENIGN")
    X_benign_train = X_train[benign_mask_train]

    print(f"[*] Calibrating Isolation Forest on {len(X_benign_train)} normal traffic baseline flows...")
    iso_forest = IsolationForest(
        n_estimators=100,
        contamination=0.01,
        random_state=42,
        n_jobs=-1
    )
    iso_forest.fit(X_benign_train)
    joblib.dump(iso_forest, os.path.join(MODELS_DIR, "isolation_forest.joblib"))
    print("[+] Isolation Forest Anomaly Engine successfully trained and serialized.")

    # -------------------------------------------------------------
    # 4. EXPLAINABLE AI (XAI): SHAP TreeExplainer
    # -------------------------------------------------------------
    print("\n" + "="*70)
    print("STEP 4: Initializing Fast TreeSHAP Explainer")
    print("="*70)
    try:
        # Initialize TreeExplainer on binary model with background summary
        background_sample = X_train[np.random.choice(len(X_train), size=min(100, len(X_train)), replace=False)]
        explainer = shap.TreeExplainer(best_binary_model, data=background_sample)
        joblib.dump(explainer, os.path.join(MODELS_DIR, "shap_explainer.joblib"))
        print("[+] SHAP TreeExplainer initialized and saved.")
    except Exception as e:
        print(f"[!] Note on SHAP serialization: {e}. Will compute on-the-fly via TreeExplainer.")

    # -------------------------------------------------------------
    # 5. EXPORT COMPREHENSIVE METRICS SUMMARY
    # -------------------------------------------------------------
    metrics_summary = {
        "binary_model_name": best_model_name,
        "model_comparisons": comparison_results,
        "feature_importances": feature_importances,
        "mitre_mappings": MITRE_MAPPINGS,
        "multiclass_evaluation": {
            "accuracy": round(multi_acc * 100, 2),
            "classes": attack_classes,
            "confusion_matrix": multi_cm,
            "per_class_metrics": {
                cls: {
                    "precision": round(rep[cls]["precision"] * 100, 1),
                    "recall": round(rep[cls]["recall"] * 100, 1),
                    "f1_score": round(rep[cls]["f1-score"] * 100, 1),
                    "support": rep[cls]["support"],
                    "mitre_id": MITRE_MAPPINGS.get(cls, {}).get("technique_id", "N/A"),
                    "cvss": MITRE_MAPPINGS.get(cls, {}).get("cvss", 0.0)
                }
                for cls in attack_classes
            }
        }
    }

    metrics_file = os.path.join(MODELS_DIR, "metrics_summary.json")
    with open(metrics_file, "w") as f:
        json.dump(metrics_summary, f, indent=2)

    print(f"\n[+] Successfully generated full metrics report at {metrics_file}")
    print("[+] Model Pipeline Execution Finished Successfully!")

if __name__ == "__main__":
    train_and_export()
