# Publishing AI-Based Student Performance Prediction on Kaggle

This guide provides two easy ways to publish your project on [Kaggle](https://www.kaggle.com/).

---

## Method 1: Instant Web Upload (Recommended — No API Key Required)

This is the fastest method (takes less than 1 minute directly in your browser).

### Option A: Publish as a Kaggle Notebook (Code)
1. Go to **[https://www.kaggle.com/code](https://www.kaggle.com/code)** and log in.
2. Click the blue **"+ New Notebook"** button on the top right.
3. In the notebook editor menu at the top, click **File** -> **Upload Notebook**.
4. Browse and select your file:
   `e:\Student Prediction\student_performance_analysis.ipynb`
   *(or `e:\Student Prediction\kaggle\kernel\student_performance_analysis.ipynb`)*
5. The notebook will load with all documentation, Markdown cells, data visualizations, and model benchmarks.
6. Under **Notebook Options** on the right panel, attach the UCI Student Performance dataset or add `student-mat.csv` / `student-por.csv`.
7. Click **Save Version** -> select **"Save & Run All (Commit)"**.
8. Once saved, go to the notebook sharing settings and change from **Private** to **Public**.

---

### Option B: Publish as a Kaggle Dataset
1. Go to **[https://www.kaggle.com/datasets](https://www.kaggle.com/datasets)** and click **"+ New Dataset"**.
2. Enter the title: `Student Performance Prediction Dataset (UCI Benchmark)`.
3. Drag & drop the files from:
   `e:\Student Prediction\kaggle\dataset\`
   - `student-mat.csv`
   - `student-por.csv`
   - `README.md`
4. Click **Create** and set visibility to **Public**.

---

## Method 2: Automated via Kaggle CLI (Terminal)

We have already installed the official `kaggle` package.

### Step 1: Authenticate with Kaggle
Choose either:
- **Interactive Browser Login**: Run in your terminal:
  ```powershell
  kaggle auth login
  ```
- **OR API Token File**:
  1. Visit [https://www.kaggle.com/settings](https://www.kaggle.com/settings).
  2. Scroll down to the **API** section and click **"Create New Token"**.
  3. A file named `kaggle.json` will download.
  4. Place it in:
     `C:\Users\KARTHICK\.kaggle\kaggle.json`

### Step 2: Set Your Kaggle Username
Open [`kaggle/kernel/kernel-metadata.json`](file:///e:/Student%20Prediction/kaggle/kernel/kernel-metadata.json) and replace `INSERT_YOUR_KAGGLE_USERNAME` with your actual Kaggle username (e.g. `karthick/student-performance-prediction-ai`).

### Step 3: Push Notebook & Dataset
Run:
```powershell
# Push the Notebook to Kaggle Code
kaggle kernels push -p "e:\Student Prediction\kaggle\kernel"

# Push the Dataset to Kaggle Datasets
kaggle datasets create -p "e:\Student Prediction\kaggle\dataset"
```
