import json
from pathlib import Path

NB_PATH = Path(__file__).resolve().parent.parent / "Model_Teacheable_Machine_EGADE.ipynb"

def make_markdown_cell(lines):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [l if l.endswith("\n") else l+"\n" for l in lines],
    }

def make_code_cell(code):
    # Accept either str or list[str]
    if isinstance(code, str):
        src = [(line + "\n") for line in code.splitlines()]
    else:
        src = code
    return {
        "cell_type": "code",
        "metadata": {},
        "source": src,
        "outputs": [],
        "execution_count": None,
    }

def main():
    nb = json.loads(NB_PATH.read_text(encoding="utf-8"))

    # 1) Modify professor's main code cell to load local SavedModel and map to 3 classes
    def replace_prof_cell():
        target_idx = None
        for i, c in enumerate(nb.get("cells", [])):
            if c.get("cell_type") == "code":
                src = "".join(c.get("source", []))
                if "tf.saved_model.load" in src and "/content/manita.png" in src:
                    target_idx = i
                    break
        if target_idx is None:
            return False

        new_prof = r"""
# ================================
# 1. Librerías
# ================================
import os
import tensorflow as tf
import numpy as np
import cv2
import matplotlib.pyplot as plt

print("TensorFlow:", tf.__version__)

# ================================
# 2. Cargar modelo SavedModel (local)
# ================================
# Carga el SavedModel exportado por el entrenamiento local en 'model_from_src'
local_model_path = os.path.join(os.getcwd(), "model_from_src")
fallback_model_path = "/content/model"  # por compatibilidad si usas Colab

model_path = local_model_path if tf.io.gfile.exists(local_model_path) else fallback_model_path
try:
    model = tf.saved_model.load(model_path)
    print("SavedModel cargado desde:", model_path)
except Exception as e:
    print(f"Error cargando SavedModel: {e}")
    model = None

infer = None
if model is not None:
    try:
        infer = model.signatures["serving_default"]
        print("Usando firma 'serving_default'.")
        print("Firma de entrada esperada:")
        for input_name, input_spec in infer.structured_input_signature[1].items():
            print(f"  Entrada '{input_name}': {input_spec}")
    except Exception as e:
        print("No se pudo obtener la firma:", e)

# ================================
# 3. Leer imagen (de src/ si existe)
# ================================
DATA_DIR = os.path.join(os.getcwd(), "src")
img_path = None

if os.path.isdir(DATA_DIR):
    # Busca una imagen cualquiera dentro de las subcarpetas de src/
    exts = (".jpg", ".jpeg", ".png", ".bmp")
    for root, _, files in os.walk(DATA_DIR):
        for f in files:
            if f.lower().endswith(exts):
                img_path = os.path.join(root, f)
                break
        if img_path:
            break

if img_path is None:
    # Fallback a la ruta usada por el profesor en Colab
    img_path = "/content/manita.png"

print("Imagen a usar:", img_path)
img = cv2.imread(img_path)

if img is None:
    print(f"Error: no se pudo cargar la imagen: {img_path}")
else:
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img_rgb)
    plt.axis("off")
    plt.show()

    # ================================
    # 4. Preparar la imagen para el modelo
    # ================================
    target_size = (224, 224)  # alto x ancho esperado por MobileNetV2
    img_resized = cv2.resize(img_rgb, target_size)
    input_tensor = tf.convert_to_tensor(np.expand_dims(img_resized, 0), dtype=tf.float32)

    # ================================
    # 5. Inferencia
    # ================================
    if infer is not None:
        print("\nEjecutando inferencia...")
        try:
            input_name = list(infer.structured_input_signature[1].keys())[0]
            outputs = infer(**{input_name: input_tensor})
            print("Claves de salida:", list(outputs.keys()))

            # ================================
            # 6. Interpretación para clasificación (3 clases)
            # ================================
            # Toma el primer tensor de salida disponible y aplica softmax
            first_key = list(outputs.keys())[0]
            logits = outputs[first_key].numpy()
            if logits.ndim == 2 and logits.shape[0] == 1:
                probs = tf.nn.softmax(logits[0]).numpy()
            else:
                probs = tf.nn.softmax(logits).numpy().squeeze()

            # Nombres de clases desde las subcarpetas de src/
            class_names = None
            if os.path.isdir(DATA_DIR):
                class_names = sorted([d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))])

            if class_names and len(class_names) == probs.shape[-1]:
                for name, p in zip(class_names, probs):
                    print(f"{name}: {p*100:.2f}%")
                pred_idx = int(np.argmax(probs))
                print("Predicción:", class_names[pred_idx])
            else:
                print("Probabilidades:", probs)

        except Exception as e:
            print("Error durante la inferencia:", e)
"""
        nb["cells"][target_idx] = make_code_cell(new_prof)
        return True

    replace_prof_cell()

    # Helpers for idempotent insertions and de-duplication
    def cell_text(c):
        return "".join(c.get("source", [])) if c.get("source") else ""

    # Unique markers for our sections/snippets
    TITLE_TRAIN = "## Entrenamiento con 3 clases (hamburguesa, omelette, pizza)"
    TITLE_LOCAL_LOAD = "## Cargar modelo local (alternativa a la celda del profesor)"
    TITLE_INFER = "## Inferencia con clases nuevas"

    SNIPPET_DATASET = "image_dataset_from_directory(\n    DATA_DIR"
    SNIPPET_MOBILENET = "tf.keras.applications.MobileNetV2(\n    input_shape=IMG_SIZE + (3,)"
    SNIPPET_SAVE = "tf.saved_model.save(model_ft, save_dir)"
    SNIPPET_LOCAL = "local_model_path = os.path.join(os.getcwd(), \"model_from_src\")"
    SNIPPET_HELPER = "def predict_with_infer("

    # 2) De-duplicate previously inserted cells by title/snippet, keeping first occurrence
    seen_titles = set()
    seen_snippets = set()
    filtered = []
    removed = 0
    for c in nb.get("cells", []):
        text = cell_text(c)

        # Check title duplicates (markdown)
        title = None
        if c.get("cell_type") == "markdown":
            if TITLE_TRAIN in text:
                title = TITLE_TRAIN
            elif TITLE_LOCAL_LOAD in text:
                title = TITLE_LOCAL_LOAD
            elif TITLE_INFER in text:
                title = TITLE_INFER
        if title:
            if title in seen_titles:
                removed += 1
                continue
            seen_titles.add(title)
            filtered.append(c)
            continue

        # Check code snippet duplicates
        if c.get("cell_type") == "code":
            key = None
            if SNIPPET_DATASET in text:
                key = "DATASET"
            elif SNIPPET_MOBILENET in text:
                key = "MOBILENET"
            elif SNIPPET_SAVE in text:
                key = "SAVE"
            elif SNIPPET_LOCAL in text:
                key = "LOCAL"
            elif SNIPPET_HELPER in text:
                key = "HELPER"
            if key:
                if key in seen_snippets:
                    removed += 1
                    continue
                seen_snippets.add(key)
                filtered.append(c)
                continue

        # Not our managed cells, keep as-is
        filtered.append(c)

    if removed:
        print(f"Removed duplicate injected cells: {removed}")
    nb["cells"] = filtered

    # 3) Append our sections only if missing
    have_train = any(TITLE_TRAIN in cell_text(c) for c in nb["cells"])
    have_local = any(TITLE_LOCAL_LOAD in cell_text(c) for c in nb["cells"])
    have_infer = any(TITLE_INFER in cell_text(c) for c in nb["cells"])

    new_cells = []

    if not have_train:
        new_cells.append(make_markdown_cell([
            TITLE_TRAIN,
            "Este bloque usa las imágenes en `src/` y entrena un modelo con MobileNetV2.",
        ]))

    code1 = r"""
# Configurar dataset desde carpeta local src/
import os, tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt

DATA_DIR = os.path.join(os.getcwd(), "src")
IMG_SIZE = (224, 224)
BATCH_SIZE = 16
VAL_SPLIT = 0.2
SEED = 1337

train_ds = tf.keras.utils.image_dataset_from_directory(
    DATA_DIR,
    validation_split=VAL_SPLIT,
    subset="training",
    seed=SEED,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int",
)
val_ds = tf.keras.utils.image_dataset_from_directory(
    DATA_DIR,
    validation_split=VAL_SPLIT,
    subset="validation",
    seed=SEED,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int",
)

class_names = train_ds.class_names
print("Clases:", class_names)

AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.prefetch(AUTOTUNE)
val_ds = val_ds.prefetch(AUTOTUNE)
"""
    if not have_train:
        new_cells.append(make_code_cell(code1))

    code2 = r"""
# Transfer learning: MobileNetV2 congelada + cabeza densa para 3 clases
base = tf.keras.applications.MobileNetV2(
    input_shape=IMG_SIZE + (3,), include_top=False, weights="imagenet"
)
base.trainable = False

inputs = keras.Input(shape=IMG_SIZE + (3,))
x = tf.keras.applications.mobilenet_v2.preprocess_input(inputs)
x = base(x, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.2)(x)
outputs = layers.Dense(len(class_names), activation="softmax")(x)
model_ft = keras.Model(inputs, outputs)

model_ft.compile(
    optimizer=keras.optimizers.Adam(1e-3),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)

EPOCHS = 5
history = model_ft.fit(train_ds, validation_data=val_ds, epochs=EPOCHS)
"""
    if not have_train:
        new_cells.append(make_code_cell(code2))

    code3 = r"""
# Guardar el modelo en formato SavedModel para reutilizarlo en la celda del profesor
save_dir = os.path.join(os.getcwd(), "model_from_src")
try:
    tf.saved_model.save(model_ft, save_dir)
    print("SavedModel exportado en:", save_dir)
except Exception as e:
    print("Error al guardar SavedModel:", e)
"""
    if not have_train:
        new_cells.append(make_code_cell(code3))

    # Opción: cargar el modelo local guardado para obtener "infer"
    if not have_local:
        new_cells.append(make_markdown_cell([
            TITLE_LOCAL_LOAD,
            "Carga el SavedModel exportado en `model_from_src` y expone la firma `infer`.",
        ]))
    code_local = r"""
# Cargar modelo local desde 'model_from_src' (alternativa a la celda del profesor)
local_model_path = os.path.join(os.getcwd(), "model_from_src")
try:
    local_model = tf.saved_model.load(local_model_path)
    infer = local_model.signatures["serving_default"]
    print("Modelo local cargado. Firma 'serving_default' disponible.")
except Exception as e:
    print("No se pudo cargar el modelo local:", e)
"""
    if not have_local:
        new_cells.append(make_code_cell(code_local))

    if not have_infer:
        new_cells.append(make_markdown_cell([
            TITLE_INFER,
            "Usa la celda del profesor para cargar el SavedModel, y esta celda para mapear probabilidades a nombres de clase.",
        ]))

    code4 = r"""
# Si ya tienes "infer" del SavedModel cargado, interpreta la salida como softmax y mapea a class_names.
import numpy as np
import cv2

def predict_with_infer(img_path, target_size=(224,224)):
    if "infer" not in globals() or infer is None:
        print("Primero carga el modelo (firma 'serving_default').")
        return
    img = cv2.imread(img_path)
    if img is None:
        print("No se pudo leer la imagen:", img_path)
        return
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(img_rgb, target_size)
    input_tensor = tf.convert_to_tensor(np.expand_dims(img_resized, 0), dtype=tf.float32)

    input_name = list(infer.structured_input_signature[1].keys())[0]
    outputs = infer(**{input_name: input_tensor})

    # Intenta tomar el primer tensor de salida disponible
    first_key = list(outputs.keys())[0]
    logits = outputs[first_key].numpy()
    if logits.ndim == 2 and logits.shape[0] == 1:
        probs = tf.nn.softmax(logits[0]).numpy()
    else:
        probs = tf.nn.softmax(logits).numpy().squeeze()

    if 'class_names' in globals():
        for i,p in enumerate(probs):
            print(f"{class_names[i]}: {p*100:.2f}%")
        pred_idx = int(np.argmax(probs))
        print("Predicción:", class_names[pred_idx])
    else:
        print("Probabilidades:", probs)

# Ejemplo de uso (ajusta a una imagen de tu carpeta):
# predict_with_infer(os.path.join(DATA_DIR, 'hamburguesa', 'cheeseburger.jpg'))
"""
    if not have_infer:
        new_cells.append(make_code_cell(code4))

    # Append new cells keeping professor's code
    nb["cells"].extend(new_cells)

    NB_PATH.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Notebook updated with training + inference helper cells.")

if __name__ == "__main__":
    main()
