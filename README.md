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

All converted images are saved in the backend directory at `static/results/`.
You can access them directly via URL: `http://127.0.0.1:5000/static/results/<filename>`

---

## 💡 Notes

- Ensure both **Flask server** and **React frontend** are running concurrently  
- Do not include spaces in image filenames (use underscores)  
- Always use grayscale MRI scans for better output quality

---

## 📫 Contact

Developed by **Muhammad Sharjeel** with ❤️  
Feel free to fork, raise issues, or contribute on [GitHub](https://github.com/msharjeel7/T1_T2-MRI-Conversion-Web-App)

