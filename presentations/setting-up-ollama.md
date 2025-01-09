---
marp: true
theme: default
paginate: true
backgroundColor: #cac
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

## **Setting Up Ollama for Local Development**

---

# Introduction

This guide will show you how to download, install, and utilize Ollama across Mac OS X, Windows and Linux

---

# What is Ollama?

**Ollama** is a lightweight, extensible framework for building and running language models on your local machine. It provides a simple API for creating, running, and managing models, along with a library of pre-built models for various applications.

---

# Download and Install Ollama

## Mac

1. **Download** the latest release from the [Ollama GitHub repository](https://github.com/ollama/ollama).
2. **Open Terminal** and navigate to the download location.
3. **Install** by running:

```bash
   sudo installer -pkg ollama-macos.pkg -target /
```

---

# Windows
Download the installer from the Ollama GitHub repository.

Run the installer and follow the on-screen instructions.

---
# Linux
Download the appropriate package from the Ollama GitHub repository.

Open Terminal and navigate to the download location.

Install by running:

```bash
sudo dpkg -i ollama-linux.deb
```

For RPM based systems

```bash
sudo rpm -i ollama-linux.rpm

```

---

## Using the Ollama CLI

To download specific models, use the `ollama pull` command followed by the model name. For example:

* **Llama 3.1**
  ```bash
  ollama pull llama3.2
  ```

* **Mistral**
  ```bash
  ollama pull mistral
  ```

* **Phi**
  ```bash
  ollama pull phi3
  ```

---

# Listing Available Models

To list all models available in the Ollama CLI, use the following command:

```bash
ollama list
```

This command will display all models currently available on your system. 

---

# Running a Model

To run a model and generate a response, use the `ollama run` command followed by the model name and your prompt. For example:

```bash
ollama run llama3.2 "Why is the sky blue?"
```

This command will generate a response based on the input prompt. 

---

# Conclusion

You've now learned how to:

- Download and install Ollama on Mac, Windows, and Linux.
- Use the CLI to download various models.
- List all available models in the Ollama CLI.

For more information and advanced usage, visit the [Ollama GitHub repository](https://github.com/ollama/ollama).


