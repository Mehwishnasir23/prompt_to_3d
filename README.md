# 🚀 PROMPT3D: Instant Neural Asset Studio

**PROMPT3D** is an advanced Generative AI platform designed to transform natural language descriptions into high-fidelity 3D meshes. By bridging the gap between Large Language Models (LLMs) and Neural Radiance Fields (NeRFs), the system allows users to generate, inspect, and export 3D assets in seconds.

---

## ✨ Key Features
* **Text-to-Mesh Synthesis:** Generate 3D geometry directly from natural language prompts using point-cloud diffusion.
* **Real-time Viewport:** Interactive 3D inspection using **Three.js** and WebGL for seamless rotation, scaling, and lighting adjustment.
* **Multi-Format Export:** Support for `.OBJ`, `.GLB`, and `.STL` formats, making assets ready for game engines (Unity/Unreal) or 3D printing.
* **Cloud Persistence:** Secure asset management and metadata storage via **Firebase Cloud Firestore**.
* **Robust Authentication:** Integrated **Firebase Auth** for secure user onboarding and private project libraries.

---

## 🛠 Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | React.js, Three.js, Tailwind CSS |
| **Backend** | Python, Flask API |
| **AI Model** | Point-E / Shap-E (Neural Synthesis) |
| **Database** | Firebase Firestore |
| **Auth** | Firebase Auth |
| **Version Control** | Git / GitHub |

---

## 📁 Project Structure

```bash
PROMPT3D/
├── client/                # React Frontend (User Interface)
│   ├── src/
│   │   ├── components/    # 3D Viewport and UI Dashboard elements
│   │   └── hooks/         # Custom hooks for asynchronous API calls
├── server/                # Flask Backend (AI Logic Engine)
│   ├── app.py             # Main REST API entry point
│   ├── model_loader.py    # Scripts for loading AI model weights
│   └── utils/             # Mesh processing and format conversion utilities
├── models/                # Pre-trained AI model weight files (LFS)
└── docs/                  # System architecture diagrams and technical manuals
