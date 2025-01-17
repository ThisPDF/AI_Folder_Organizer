import os
import shutil
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import SGDClassifier  # Supports incremental learning
import pickle

TRAINING_DATA_FILE = "training_data.pkl"
MODEL_FILE = "model.pkl"
VECTORIZER_FILE = "vectorizer.pkl"

def load_training_data():
    if os.path.exists(TRAINING_DATA_FILE):
        with open(TRAINING_DATA_FILE, "rb") as f:
            return pickle.load(f)
    return [], []

def save_training_data(file_names, folder_labels):
    with open(TRAINING_DATA_FILE, "wb") as f:
        pickle.dump((file_names, folder_labels), f)

def load_model():
    if os.path.exists(MODEL_FILE) and os.path.exists(VECTORIZER_FILE):
        with open(MODEL_FILE, "rb") as f:
            model = pickle.load(f)
        with open(VECTORIZER_FILE, "rb") as f:
            vectorizer = pickle.load(f)
        return model, vectorizer
    return None, None

def save_model(model, vectorizer):
    with open(MODEL_FILE, "wb") as f:
        pickle.dump(model, f)
    with open(VECTORIZER_FILE, "wb") as f:
        pickle.dump(vectorizer, f)

def analyze_user_patterns(selected_paths):
    import random  # Import random to sample files

    # Load existing training data
    file_names, folder_labels = load_training_data()

    max_files_per_folder = 100  # Limit the number of files per folder

    for target_path in selected_paths:
        for root, dirs, files in os.walk(target_path):
            # Randomly sample files if more than max_files_per_folder
            if len(files) > max_files_per_folder:
                files = random.sample(files, max_files_per_folder)
            for file in files:
                file_names.append(file)
                folder_labels.append(os.path.basename(root))
            # Optionally, break after processing subdirectories to limit data
            # break

    if len(set(folder_labels)) < 2 or len(file_names) < 10:
        return None, None

    # Vectorize file names
    vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 4), lowercase=True)
    X = vectorizer.fit_transform(file_names)

    # Train the model (using SGDClassifier for incremental learning)
    model = SGDClassifier(max_iter=1000, tol=1e-3, random_state=42)
    model.fit(X, folder_labels)

    # Save the updated training data and model
    save_training_data(file_names, folder_labels)
    save_model(model, vectorizer)

    return model, vectorizer

def train_default_model():
    # Load existing training data
    file_names, folder_labels = load_training_data()

    if not file_names:
        # If no existing data, use default training data
        training_data = {
            "Documents": ["doc", "pdf", "text", "notes", "txt", "rtf"],
            "Media": ["photo", "image", "video", "music", "audio", "jpg", "png"],
            "Code": ["code", "source", "script", "python", "java", "js", "html"],
            "Archives": ["archive", "zip", "rar", "7z"],
            "Others": ["misc", "temp", "download", "stuff"]
        }
        file_names = [name for names in training_data.values() for name in names]
        folder_labels = [category for category, names in training_data.items() for _ in names]

    # Vectorize file names
    vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 4), lowercase=True)
    X = vectorizer.fit_transform(file_names)

    # Train the model
    model = SGDClassifier(max_iter=1000, tol=1e-3, random_state=42)
    model.fit(X, folder_labels)

    # Save the model and vectorizer
    save_model(model, vectorizer)

    return model, vectorizer

def organize_items_ml(target_path, model, vectorizer, progress_callback=None):
    items = [f for f in target_path.iterdir() if f.is_file()]
    total_items = len(items)
    processed_items = 0

    for item in items:
        try:
            item_vec = vectorizer.transform([item.name])
            category = model.predict(item_vec)[0]
            target_folder = target_path / category
            target_folder.mkdir(exist_ok=True)
            destination = target_folder / item.name
            if item.parent.resolve() != target_folder.resolve():
                shutil.move(str(item), str(destination))
        except Exception as e:
            print(f"Error moving item {item}: {e}")
        processed_items += 1
        if progress_callback:
            progress_callback(processed_items / total_items * 100)
