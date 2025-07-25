# 🧠 T1 ↔ T2 MRI Image Conversion Web App

This intuitive web app enables seamless conversion between **T1-weighted** and **T2-weighted** MRI images using a pre-trained **CycleGAN** model 🌀.  
Designed for ease of use, it offers live previews and high-quality outputs — all in your browser.

---

## 🚀 Key Features

- 📤 Upload one or multiple grayscale MRI images (PNG)
- 🔁 Convert between **T1 → T2** and **T2 → T1**
- 🖼️ Instantly preview both uploaded and converted images
- 📥 Converted images are auto-saved in the backend
- ⚙️ Built using **React** (Frontend) & **Flask + TensorFlow** (Backend)

---

## 🛠️ Tech Stack

- **Frontend:** React.js, Tailwind CSS, Axios, Toastify  
- **Backend:** Python, Flask, TensorFlow, TensorFlow Addons  
- **Other:** Pillow for image handling, NumPy for array processing

---

## 📦 How to Use

1. Clone the repository and install both frontend and backend dependencies  
2. Upload grayscale MRI images  
3. Select conversion direction: `T1 → T2` or `T2 → T1`  
4. Click **Convert**  
5. Preview converted images and download if satisfied  

---

## 📁 Output Location

All converted images are saved in the backend directory at:

