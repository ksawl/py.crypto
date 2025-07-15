# Encryption and Decryption Tool

A Python-based tool for securely encrypting and decrypting text using the AES and RSA algorithms. This project provides a simple graphical interface for encrypting and decrypting data. It uses the `pycryptodome` library for secure encryption and `tkinter` to handle the user interface.

---

## **Doc**

-   (Tkinter)[https://tkdocs.com/tutorial/intro.html]
-   (PyCryptodome)[https://pycryptodome.readthedocs.io/en/latest/src/introduction.html]
-   (Stop using RSA)[https://habr.com/ru/companies/virgilsecurity/articles/459370/]

---

## **Features**

-   Supports **AES** and **RSA** encryption algorithms.
-   Digital signatures, used to guarantee integrity and non-repudiation.
-   Easy-to-use interface for encryption and decryption processes.

---

## **Installation**

### **Prerequisites**

1. Python 3.7 or above installed on your system.
2. Required Python libraries:
    - `pycryptodome`

### **Install Dependencies**

This project uses [Poetry](https://python-poetry.org/) to manage dependencies and run the script. Follow these steps to execute `main.py`:

#### **1. Prerequisites**

-   [Python 3.8+](https://www.python.org/downloads/)
-   [Poetry installed](https://python-poetry.org/docs/#installation)

#### **2. Install Dependencies**

Clone the repository and install dependencies (skip installing the project itself since it’s a single script):

```bash
git clone https://github.com/ksawl/py.crypto
cd py.crypto
poetry install --no-root
```

#### **3. Run the Script**

Execute `main.py` directly in Poetry’s virtual environment:

```bash
poetry run python main.py
```

#### **4. Optional: Use Poetry Shell**

Activate the virtual environment first (useful for repeated runs):

```bash
poetry shell
python main.py
```

---

### **Troubleshooting**

-   **Error about missing package**:  
    If you see an error like `No file/folder found for package`, it’s because Poetry expects a package structure by default. We avoid this by using `--no-root` in `poetry install`.

-   **Missing dependencies**:  
    Ensure all dependencies are listed in `pyproject.toml` and re-run `poetry install`.
