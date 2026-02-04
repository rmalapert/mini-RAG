# Mini RAG - Système de Recherche avec Retrieval Augmented Generation

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

Un système RAG (Retrieval Augmented Generation) permettant de charger des documents PDF, de créer une base vectorielle pour la recherche sémantique, et d'effectuer des requêtes intelligentes sur vos documents.

## 📋 Description

Mini RAG est un système de Retrieval Augmented Generation qui combine:
- **LangChain**: Framework pour les applications LLM
- **ChromaDB**: Base de données vectorielle pour stocker les embeddings
- **Azure OpenAI**: Génération des embeddings vectoriels
- **PyMuPDF**: Extraction de texte depuis les PDFs
- **EasyOCR**: OCR automatique pour les PDFs scannés (fallback intelligent)

Le système charge automatiquement vos documents PDF, extrait le texte (avec OCR si nécessaire), crée des embeddings vectoriels et permet une recherche sémantique avancée avec MMR (Maximal Marginal Relevance).

## ✨ Fonctionnalités

- 📄 **Chargement intelligent de PDFs**: Extraction de texte avec PyMuPDF
- 🔍 **OCR automatique**: Bascule automatiquement vers EasyOCR pour les PDFs scannés
- 🇫🇷 **Support du français**: OCR configuré pour la langue française
- 🗄️ **Base vectorielle ChromaDB**: Stockage persistant des embeddings
- 🎯 **Recherche sémantique**: Retriever MMR pour des résultats diversifiés et pertinents
- ☁️ **Embeddings Azure OpenAI**: Intégration avec Azure OpenAI pour des embeddings de qualité

## 📁 Structure du projet

```
mini-RAG/
├── README.md
├── requirements.txt
├── questions_test.txt
├── .gitignore
├── data/
│   └── pdf/                    # Placez vos PDFs ici
├── src/
│   ├── __init__.py
│   ├── pdf_loader.py           # Chargement des PDFs avec OCR
│   ├── vector_langchain.py     # Création du vector store
│   └── embedding/
└── utils/
```

## 🔧 Installation

```bash
# Cloner le repository
git clone https://github.com/rmalapert/mini-RAG.git
cd mini-RAG

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

## ⚙️ Configuration

Créer un fichier `.env` à la racine du projet avec vos credentials Azure OpenAI:

```env
OPENAI_API_KEY=votre_cle_api
AZURE_OPENAI_ENDPOINT=votre_endpoint
DEPLOYMENT_NAME_EMBEDDING=nom_du_deployment
OPENAI_API_VERSION=2024-02-15-preview
```

⚠️ **Important**: Le fichier `.env` est déjà inclus dans `.gitignore` pour éviter de commiter vos secrets.

## 🚀 Utilisation

### Préparer vos données

```bash
# Placer vos fichiers PDF dans le dossier data/pdf/
mkdir -p data/pdf
cp vos_fichiers.pdf data/pdf/
```

### Créer le vector store

```python
from src.vector_langchain import vector_store, retriever

# Le vector store est créé automatiquement au premier lancement
# Les documents sont indexés depuis data/pdf/

# Utiliser le retriever pour rechercher
results = retriever.get_relevant_documents("votre question ici")
for doc in results:
    print(doc.page_content)
```

### Mettre à jour le vector store

Pour réindexer vos documents après avoir ajouté/modifié des PDFs:

1. Modifier `MAJ_VS = True` dans `src/vector_langchain.py`
2. Relancer le script

## 📦 Dépendances principales

- `langchain` et `langchain-community`: Framework RAG
- `langchain-openai`: Intégration Azure OpenAI
- `chromadb`: Base de données vectorielle
- `PyMuPDF` (fitz): Extraction de texte PDF
- `easyocr`: OCR pour PDFs scannés
- `python-dotenv`: Gestion des variables d'environnement

## 🔍 Fonctionnement

### pdf_loader.py
- Charge les PDFs avec PyPDFLoader
- Détecte automatiquement si le texte extrait est insuffisant
- Bascule vers EasyOCR pour une extraction par OCR si nécessaire
- Retourne une liste de documents LangChain

### vector_langchain.py
- Split les documents en chunks avec RecursiveCharacterTextSplitter
- Crée les embeddings avec Azure OpenAI
- Stocke les embeddings dans ChromaDB
- Configure un retriever MMR pour la recherche

## 📝 Notes

- Le dossier `vectorstore_db/` est créé automatiquement pour stocker la base vectorielle
- Le fichier `questions_test.txt` contient des exemples de questions de test
- L'OCR est configuré pour le français (`['fr']`)
- GPU désactivé par défaut pour EasyOCR (configurez `gpu=True` si disponible)
- Le retriever utilise MMR avec k=5 documents par défaut

## 🤝 Contribution

Les contributions sont les bienvenues! N'hésitez pas à:
- Ouvrir une issue pour signaler un bug ou proposer une fonctionnalité
- Soumettre une pull request pour améliorer le code

## 📄 License

Ce projet est disponible sous license MIT. Voir le fichier LICENSE pour plus de détails.