# 📚 Advanced Lecture Scripts: From Pixels to Text (v2)
## Course: Document AI & Pattern Recognition
**Lecturer:** Muhamadxon Mahmudov, PhD AI Researcher & Assistant Teacher (Kokand University & ALTAIIM Research Center) [a293d80e]
**Language:** English (For International Students)
**Target:** 80-Minute High-Fidelity Lecture (Period 1)

---

## 🎬 Slide 1: Welcome & Speaker Profile
*   **Visual Representation:** Split-screen layout. Left: Presenter profile featuring Kokand University and ALTAIIM Research Center branding [a293d80e]. Right: An abstract graphic showing a 2D matrix of raw pixel values (0-255) dynamically morphing into clean, digitized Uzbek Latin characters.
*   **Slayd Tezers (Slide Bullet Points):**
    *   **Lecturer:** Muhamadxon Mahmudov [a293d80e]
    *   **Academic Affiliation:** Department of Computer Engineering & Digital Technologies, Kokand University (Andijan Branch) [a293d80e]
    *   **Research Affiliation:** Lead AI/NLP Engineer at ALTAIIM Research Center (Specialty 05.01.11 - AI and Digital Technologies) [a293d80e]
    *   **Core Scientific Objective:** Building the 500,000-word "Intellectual Thesaurus Dictionary of the Uzbek Language" digital platform [a293d80e]
    *   **The Document AI Bottleneck:** Digitizing centuries of print archives, historical lexicons, and regional manuscripts into searchable data [a293d80e]
*   **Lecturer's Script (English):**
    > "Good morning, everyone! Welcome to Kokand University's Andijan branch [a293d80e]. My name is **Muhamadxon Mahmudov**, and I am an assistant teacher here at the Department of Computer Engineering [a293d80e]. It is an absolute privilege to welcome you to this advanced session on Document AI.
    > 
    > To give you a brief context about my background: besides lecturing on 'Data Structures and Algorithms', my primary PhD research centers on Artificial Intelligence and Natural Language Processing [a293d80e]. Under the leadership of Professor Mukhtorxon Umarxoja'yev at the ALTAIIM Research Center, my team and I are currently building a massive 500,000-word digital thesaurus platform for the Uzbek language [a293d80e]. 
    > 
    > Why is this relevant to today's topic? Because in large-scale NLP and translation projects, our absolute first bottleneck is data ingestion. We cannot analyze or model language until we extract it from physical print archives, historical dictionaries, and regional manuscripts. Converting these scanned documents into high-fidelity, machine-readable text is where Optical Character Recognition—or OCR—becomes the vital bridge. Today, we will explore the deep mathematical and structural mechanics of how computers see shapes, how neural networks model characters, and how modern Vision-Language Models parse documents without even using traditional OCR engines, mapping these architectures directly to the orthographic challenges of the Uzbek Latin script. Let's begin!"

---

## 📜 Slide 2: OCR History & Origins: Yann LeCun, LeNet-5 & MNIST (1998)
*   **Visual Representation:** An archival photograph of Yann LeCun at AT&T Bell Laboratories [f55f9680] alongside a grid of handwritten digits from the legendary **MNIST dataset** (28x28 grayscale matrices) [b16ca527], and a schematic of the AT&T DSP-32C check-reading system (HCAR50) [274].
*   **Slayd Tezers (Slide Bullet Points):**
    *   **Yann LeCun:** Turing Award laureate (2018) and pioneer of Convolutional Neural Networks (CNNs) [f55f9680, 366]
    *   **LeNet-5 (1998):** The foundational CNN designed to automate handwritten zip code and bank check recognition [b16ca527, f09db86d, 272]
    *   **The MNIST Standard:** 70,000 size-normalized, centered $28 	imes 28$ grayscale images [b16ca527, 24]
    *   **Industrial Impact:** Deployed by NCR in ATMs, processing 20 million checks per day (10% of all US checks) in the late 1990s [274, 367]
    *   **Local Relevance:** Establishing benchmarks for handwritten datasets—comparing global MNIST [24] against local Uzbek handwriting (ASU-HWDD, 2025) [20, 21].
*   **Lecturer's Script (English):**
    > "To understand where modern document intelligence stands, we must go back to AT&T Bell Laboratories in the late 1980s and 90s [f55f9680, 272, 367]. Before this era, Optical Character Recognition was highly fragile. It relied on hand-designed, rules-based template matching [120, b16ca527]. If a character had a slight rotation, minor ink bleed, or unexpected line thickness, template matching failed entirely [b16ca527, 120]. 
    > 
    > Yann LeCun, who completed his PhD on connectionist learning models and a postdoc under Geoffrey Hinton, changed everything [253, 364]. Instead of manually engineering rules for every shape, his team built a machine that learned features directly from raw pixel grids [119, b16ca527]. To train and benchmark this network, they developed the **MNIST dataset**—a collection of 70,000 handwritten digits [24]. 
    > 
    > By training **LeNet-5**, a specialized multi-layer neural network with backpropagation, they achieved record accuracy [b16ca527, 115, 272]. This wasn't just a theoretical breakthrough; it was a major industrial success. Deployed on AT&T's DSP-32C floating-point processors under the HCAR50 system, LeNet-5 automatically read the numerical amounts on millions of bank checks per day—about 10% of the US total [274, 117].
    > 
    > Interestingly, in our own department at Andijon State University, we conducted similar experiments [20]. We designed the **ASU-HWDD** (Andijan State University Handwritten Digits Dataset) to evaluate how these historical neural architectures generalize to Uzbek handwriting, where students wrote under no strict constraints [21, 26, 53]. This highlights that handwritten character recognition remains a core touchstone of visual AI history [21]."

---

## ⚙️ Slide 3: CNN Mechanics: Local Receptive Fields & Weight Sharing
*   **Visual Representation:** The classic **LeNet-5 architecture diagram**: Input (32x32) $ightarrow$ C1 Conv (6@28x28) $ightarrow$ S2 Average Pooling (6@14x14) $ightarrow$ C3 Conv $ightarrow$ S4 Pooling $ightarrow$ C5 Conv $ightarrow$ F6 Fully Connected $ightarrow$ Output (10 RBF classes) [b16ca527].
*   **Slayd Tezers (Slide Bullet Points):**
    *   **The CNN Blueprint:** Replacing fixed handcrafted feature extractors with automatic, end-to-end feature learning [119, 132]
    *   **Local Receptive Fields:** Neurons connect to local pixel neighborhoods to extract elementary visual features (edges, corners, stroke junctions) [133, b16ca527]
    *   **Weight Sharing (Replication):** Replicating the same weight kernel across the entire image to achieve translation invariance and reduce parameter counts [133, b16ca527]
    *   **Spatial Subsampling (Pooling):** Blurring exact spatial coordinates to gain robustness against local handwriting distortions and shifts [133, b16ca527]
*   **Lecturer's Script (English):**
    > "Let's analyze why LeNet-5 succeeded where traditional neural networks failed. If we feed a $32 	imes 32$ character image into a standard fully connected network, the first hidden layer alone would require thousands of weights, leading to rapid overfitting and massive computational costs. LeCun bypassed this using three architectural principles: local receptive fields, shared weights, and spatial subsampling [133, b16ca527].
    > 
    > First, instead of connecting every neuron to every pixel, units in LeNet-5 connect only to a small local neighborhood [133, b16ca527]. This mimics biological vision, allowing neurons to act as localized feature detectors, finding simple lines, angles, and stroke junctions [133, b16ca527].
    > 
    > Second, because a feature like a vertical stroke is useful whether it appears in the top-left or bottom-right, we force all units in a 'feature map' to share the exact same set of weights as they scan the image [133, b16ca527]. This 'weight sharing' dramatically limits the number of free parameters—allowing a network with over 340,000 connections to have only 60,000 trainable weights [134, b16ca527].
    > 
    > Third, we alternate these convolutions with average pooling or subsampling layers [133, b16ca527]. By averaging local pixel values, we reduce the spatial resolution of the feature maps [133, b16ca527]. This blurs the exact coordinates of a stroke, meaning the network doesn't care exactly where a curve is, as long as it is positioned correctly relative to the rest of the character [133, b16ca527]. This is why CNNs are robust to shifts, scales, and distortions."

---

## 📐 Slide 4: Classic OCR System Model: The Preprocessing & Segmentation Pipeline
*   **Visual Representation:** A block diagram representing the classical document image digitizing pipeline [29, 30]: 
    `Template Ingestion` $ightarrow$ `Binarization` $ightarrow$ `Corner Bounding Detection` $ightarrow$ `Homography / Bilinear Correction` $ightarrow$ `Surgical Grid Slicing` $ightarrow$ `Heatmap Quality Assurance`. 
    Include code snippets of the `find_corners` and `crop_numbers` functions from the ASU-HWDD paper [41, 50].
*   **Slayd Tezers (Slide Bullet Points):**
    *   **The Classic Workflow:** Step-by-step mathematical extraction of structured data from raw paper templates [29, 30, 63]
    *   **Image Binarization:** Converting color or grayscale scans to high-contrast binary matrices based on pixel intensity thresholds [30, 34]
    *   **Borders & Corner Detection:** Utilizing Euclidean distance and corner constraints to localize text bounding boxes [33, 38, 41]
    *   **Homography Perspective Projection:** Correcting skewed, tilted scans using bilinear interpolation to reconstruct flat grid surfaces [43, 44, 46]
    *   **Surgical Cell Slicing:** Slicing the corrected grid using padxy margins to isolate characters and omit border lines [47, 49, 50]
    *   **Heatmap QA Verification:** Visualizing character density profiles (issiqlik xaritasi) to identify segment alignment errors [30, 51, 52]
*   **Lecturer's Script (English):**
    > "Now, let's explore the **Classic OCR System Model**. Before any neural network can recognize text, we must run a strict pipeline of mathematical and image preprocessing algorithms to extract, clean, and segment our data [29, 30, 318]. 
    > 
    > To illustrate this classic workflow, let's look at the pipeline we designed for the ASU-HWDD project [20, 30]:
    > 
    > First, **Image Binarization**: We convert our scanned templates into grayscale and apply a black threshold (e.g., `< 50`) to separate background paper from foreground handwriting [34, 41]. 
    > 
    > Second, **Corner Bounding Detection**: Book pages or templates are often scanned at slight, unpredictable angles [27, 32]. We write a custom algorithm, `find_corners`, which scans the outer edges of the binarized image and uses Euclidean distance—derived from the Pythagorean theorem—to find the exact four black corner points of our printed grid [33, 38, 41]. 
    > 
    > Third, **Homography & Perspective Projection**: Since scans are often skewed, we use Pillow's `Image.transform` with `Image.QUAD` and `Image.BILINEAR` interpolation [44, 46]. This maps our skewed quadrilateral coordinates back to a perfectly flat, rectified $2080 	imes 2880$ rectangular coordinate grid [44, 45].
    > 
    > Fourth, **Surgical Cell Slicing**: Using our `crop_numbers` algorithm, we divide this rectified grid into $36 	imes 26$ character cells [25, 48, 50]. To ensure the printed black grid lines don't get mixed with the handwriting, we apply a spatial offset (`padxy=5`) to crop clean $64 	imes 64$ cells, which are subsequently scaled to $28 	imes 28$ grayscale matrices [27, 49, 50].
    > 
    > Finally, **Heatmap Quality Assurance**: We generate aggregate 'heatmaps' (issiqlik xaritasi) for all cropped digits [30, 51]. If a scan was skewed or incorrectly cropped, the heatmap will appear blurry and unfocused (like in sheet 070) [52]. If the alignment is perfect, the heatmap will showcase a sharp, high-intensity average stroke of the numbers (like in sheet 069) [52]. This classic workflow forms the bedrock of data preparation in Document AI."

---

## 📈 Slide 5: Tesseract & Baseline Spline Fitting (The "Skew" Challenge)
*   **Visual Representation:** Ray Smith's **Figure 1** showing curved fitted baselines, alongside cropped scans of distorted text lines [934b2b73]. Next to it, show a curved, skewed scanned line of the Uzbek compound phrase: ***"ijtimoiy-iqtisodiy rivojlanish"***.
*   **Slayd Tezers (Slide Bullet Points):**
    *   **Tesseract History:** Developed at HP (1984-1994), open-sourced in 2005, and maintained by Google [934b2b73]
    *   **The Spline Innovation:** Fitting a **quadratic spline** (least squares fit) to handle curved text baselines [934b2b73]
    *   **Maintaining Geometry:** Ensuring baseline, descender line, meanline, and ascender line remain parallel and equidistant [934b2b73]
    *   **Uzbek Latin Application:** Warp-effects near thick book bindings curve long words like *"ijtimoiy-iqtisodiy"*. Tesseract maps and processes these curves without destructive de-skewing [934b2b73]
*   **Lecturer's Script (English):**
    > "Now, let's transition from binarization and grid segmentation to processing full pages of unstructured text. The most famous and widely utilized open-source engine for this is Google's **Tesseract** [934b2b73]. Developed originally at Hewlett-Packard between 1984 and 1994, it was open-sourced in late 2005 [934b2b73]. One of Tesseract's most brilliant historical innovations is **Baseline Spline Fitting** [934b2b73].
    > 
    > When book pages are scanned, they are rarely perfectly straight. The text lines curve, particularly near the binding or due to camera warp [934b2b73]. Standard straight-line baseline finders would fail here, cutting through words and misidentifying layout regions [934b2b73]. Tesseract solves this by assigning filtered character blobs to lines, and fitting a **quadratic spline** across these blobs using a least median of squares fit [934b2b73]. This spline defines a curved baseline where the descender, mean, and ascender lines remain parallel at a constant vertical separation [934b2b73].
    > 
    > Think about digitizing a thick academic book containing the long Uzbek compound phrase: ***'ijtimoiy-iqtisodiy rivojlanish'***. If scanned along a curved spine, a straight line detector would split 'ijtimoiy-iqtisodiy' into two lines, ruining sentence-level NLP. Tesseract's spline bends along the curve of the characters, mapping and normalizing the entire text string perfectly without requiring destructive image rotating or de-skewing, which often degrades raw pixel quality [934b2b73]."

---

## 📌 Slide 6: The "Okina" Challenge in O‘ and G‘ (Tesseract Figure 7 - Normalization)
*   **Visual Representation:** Ray Smith's **Figure 7 (Baseline and Moment Normalized Letters)**, showing the stark visual contrast between centroid moment-normalized and baseline/x-height normalized text [934b2b73]. Highlight the Uzbek letters **O‘** and **G‘** with the floating okina ( ‘ ).
*   **Slayd Tezers (Slide Bullet Points):**
    *   **The Floating Okina ( ‘ ):** A crucial orthographic marker in Uzbek Latin (e.g., *“to‘g‘ri”*, *“g‘alaba”*, *“O‘zbekiston”*)
    *   **The Image Noise Trap:** In typical OCR pipelines, small, floating, isolated marks are often discarded as 'noise' or 'dust' [934b2b73]
    *   **Centroid Moment Normalization:** Standard static classifiers normalize characters by center of mass [934b2b73]. This removes font aspect ratio but distorts small, floating markers [934b2b73]
    *   **Isotropic Baseline/x-Height Normalization:** The Adaptive Classifier preserves the relative height of the okina to the baseline, saving it from erasure [934b2b73]
*   **Lecturer's Script (English):**
    > "Let's discuss one of the most critical and unique challenges in Uzbek Latin OCR: the floating apostrophe, or okina ( ‘ ), used in the letters **O‘** and **G‘**. In standard image binarization, tiny, isolated floating marks are highly dangerous. The algorithm often treats them as random dust specks, speckle noise, or paper defects, and wipes them out of the image [934b2b73].
    > 
    > Tesseract prevents this using its two-pass architecture and a specialized normalization strategy [934b2b73]. In the first pass, Tesseract's static classifier uses **Centroid Moment Normalization** [934b2b73]. It calculates the character's center of mass to scale and center it, which is excellent for removing font aspect ratios [934b2b73]. However, centroid shifting moves the relative position of the floating okina, confusing the classifier [934b2b73].
    > 
    > To resolve this, on the second pass, Tesseract's **Adaptive Classifier** switches to **Isotropic Baseline/x-Height Normalization** [934b2b73]. As you can see in Figure 7 of the Tesseract paper [934b2b73], baseline normalization preserves the exact vertical height of characters relative to the baseline [934b2b73]. By keeping the okina in its high-register position above the letter 'O' or 'G' in words like *'g‘alaba'* or *'to‘g‘ri'*, the engine confidently identifies it as an orthographic apostrophe rather than a random noise speck, protecting the grammatical meaning of the Uzbek text [934b2b73]."

---

## ✂️ Slide 7: Segmentation & Chopping Touching Uzbek Characters (Figure 4)
*   **Visual Representation:** Ray Smith's **Figure 4 (Candidate Chop Points and Chop)** showing the polygonal approximation of the word "arm" split by concave vertices [934b2b73]. Right next to it, display the Uzbek touching letter pairs: ***"sh"*** (in *“shahar”*), ***"ch"*** (in *“chiroy”*), and ***"tt"*** (in *“katta”*).
*   **Slayd Tezers (Slide Bullet Points):**
    *   **The Touching Character Bottleneck:** Poor print quality or ink bleed causes letters to jismonan birlashib ketish (physically touch) [934b2b73]
    *   **Concave Vertices Chopping:** Tesseract represents character outlines as polygons and detects sharp inner corners (concave vertices) as candidate split lines [934b2b73]
    *   **Uzbek Di-graphs & Double Consonants:** Splitting touching letters in digraphs like ***'sh'*** and ***'ch'*** or double letters like ***'tt'***
    *   **The A\* Associator:** Evaluates alternative cuts, using best-first search over the segmentation graph to validate Uzbek dictionary compliance [934b2b73]
*   **Lecturer's Script (English):**
    > "In real-world document digitization, characters are rarely perfectly separated [934b2b73]. In printed Uzbek, we constantly encounter touching letters—particularly in digraphs like ***'sh'*** and ***'ch'***, and double consonants like ***'tt'*** in words like ***'katta'***. If the ink bled during printing, these letters merge into a single solid blob [934b2b73].
    > 
    > How does Tesseract separate them? It uses **Concave Vertices Chopping** [934b2b73]. The engine models the connected component outline as a polygon [934b2b73]. It then scans the contour for 'concave vertices'—sharp, inward-pointing corners [934b2b73]. These corners represent the physical indentation where the circular boundary of one letter met the stroke of another [934b2b73].
    > 
    > Tesseract draws candidate split lines between opposing concave vertices [934b2b73]. It chops the blob, runs the classifier on the individual pieces, and checks if the classification confidence improves [934b2b73]. If the confidence scores are high, the split is accepted [934b2b73]. If there is ambiguity, the **A\* associator** conducts a best-first search over the segmentation graph, evaluating alternative character combinations and cross-checking them against Tesseract's internal language permuter to ensure the split results in valid Uzbek words [934b2b73]."

---

## 🩹 Slide 8: Restoring Broken Uzbek Characters (Figure 6)
*   **Visual Representation:** Ray Smith's **Figure 6 (Pristine 'h', broken 'h', features matched to prototypes)** showing how fragmented outline segments match a complete prototype [934b2b73]. Next to it, show a physically damaged Uzbek word, such as ***"bo'lim"***, where the letter **"b"** is split, visually resembling a vertical bar **"l"** and a curve **"o"**.
*   **Slayd Tezers (Slide Bullet Points):**
    *   **The Fragmentation Problem:** Aging paper and ink fade break character strokes, severing letters into disconnected parts [934b2b73]
    *   **Topological Fragility:** Traditional OCR models that rely on strict loop or junction counting fail on broken lines [934b2b73]
    *   **Many-to-One Feature Matching:** [934b2b73]
        *   *Unknown Features:* Small, localized 3D vectors (x, y position, angle) [934b2b73]
        *   *Prototype Features:* Clustered 4D vectors (x, y position, angle, length) [934b2b73]
    *   **Uzbek Reconstruction:** Fragmented letters like **'b'** or **'d'** are correctly reconstructed by matching local vectors to standard prototype templates [934b2b73]
*   **Lecturer's Script (English):**
    > "On the other end of the spectrum is the problem of **broken characters** [934b2b73]. In older, physically damaged books, ink fade and paper deterioration break character outlines [934b2b73]. A letter like **'b'** in the Uzbek word ***'bo'lim'*** might have its vertical stem severed from its loop, making it look visually like an 'l' followed by an 'o' [934b2b73]. Traditional OCR systems that rely on counting closed loops fail immediately when strokes are broken [934b2b73].
    > 
    > Tesseract solves this with a powerful mathematical paradigm: **the features extracted from the unknown character do not need to be the same as the features in the training prototypes** [934b2b73].
    > 
    > As shown in Figure 6, during classification, Tesseract extracts short, fixed-length 3D features representing local position and angle from the outlines [934b2b73]. It then maps these small, fragmented vectors **many-to-one** against the clustered, larger 4D prototype features of pristine training data [934b2b73]. 
    > 
    > Even though the gap in a broken letter 'b' leaves some prototype segments completely unmatched, the remaining features match the 'b' prototype so perfectly that the engine confidently recognizes the character [934b2b73]. This many-to-one feature matching is why Tesseract is incredibly robust when digitizing historically degraded Uzbek texts [934b2b73]."

---

## 🚀 Slide 9: Enterprise SOTA: Baidu PaddleOCR (PP-OCRv6)
*   **Visual Representation:** Baidu's multi-stage pipeline: DBNet (Text Detection) $ightarrow$ Direction Classifier (Angle Rectification) $ightarrow$ PP-OCRv6 (Text Recognition) $ightarrow$ PP-StructureV3 [102, 103]. Highlighting a multi-column table parsed smoothly into Excel and Markdown formats [102].
*   **Slayd Tezers (Slide Bullet Points):**
    *   **The Production Framework:** Industrial-grade toolkit built on Baidu's PaddlePaddle deep learning platform [95, 101]
    *   **PP-OCRv6 Efficiency:** Highly optimized neural network tiers (models as tiny as 1.5M up to 34.5M parameters) [105]
    *   **Inference Performance:** Surpassing massive vision-language models on edge hardware with 5.2x CPU speedup [103, 105]
    *   **PP-StructureV3:** Automatically analyzes document layouts, identifies headings, and extracts tables into structured Markdown/JSON [102]
*   **Lecturer's Script (English):**
    > "While Tesseract is highly scriptable for simple CPU-bound tasks, modern enterprise document processing requires handling complex layouts—like tables, receipts, invoices, and multi-column academic pages [102]. This is where Baidu’s **PaddleOCR** represents the state-of-the-art [101].
    > 
    > Unlike Tesseract's single-thread pipeline, PaddleOCR separates the workflow into highly optimized, specialized deep learning models [102]. First, a text detection network (DBNet) draws bounding boxes around text regions [102]. Next, an angle classifier checks if the text is rotated and rectifies it [102]. Finally, a compact recognition network decodes the characters [102].
    > 
    > Released recently, **PP-OCRv6** is incredibly compact, with models ranging from 1.5M to 34.5M parameters [105]. Yet, it matches or exceeds the accuracy of billion-parameter models while running up to 5.2 times faster on standard CPUs via OpenVINO [105]. Furthermore, its **PP-StructureV3** module can perform full layout analysis, extract nested table cells, merge multi-page tables, and export them directly into structured Markdown and Excel sheets [102, 106, 107]."

---

## 🧠 Slide 10: The Paradigm Shift: OCR-Free Document Transformers
*   **Visual Representation:** The end-to-end **Donut architecture flowchart**: Scanned Image $ightarrow$ Swin Transformer (Visual Encoder) $ightarrow$ High-dimensional Visual Embeddings $ightarrow$ BART (Textual Decoder) + Natural Language Prompt $ightarrow$ Structured JSON [92, 344].
*   **Slayd Tezers (Slide Bullet Points):**
    *   **The Error Propagation Problem:** Pipeline OCR errors (e.g. misreading a digit) propagate downstream, corrupting NLP data pipelines [82, 342, 375]
    *   **Donut (Document Understanding Transformer):** The first end-to-end visual transformer that entirely bypasses OCR engines [92, 344, 375]
    *   **Swin Encoder:** Splits raw document images into patches and generates visual embeddings [93, 344]
    *   **BART Decoder:** Autoregressively generates text sequences conditioned on prompt queries [93, 344]
    *   **Teacher-Forcing Training:** Trained on target sequence loss rather than previous inputs, as receipt digits have no semantic dependencies [85]
*   **Lecturer's Script (English):**
    > "But what if we skip the OCR engine entirely? Traditional OCR pipelines suffer from a fatal flaw called **Error Propagation** [82, 342, 375]. If Tesseract or PaddleOCR misreads a single digit in a financial table, the subsequent NLP database is corrupted, and a downstream LLM cannot recover the lost visual information [82, 342, 375].
    > 
    > To solve this, researchers developed **Donut** (Document Understanding Transformer)—the first **OCR-free** visual document transformer [92, 344, 375]. Donut completely removes character segmentation and bounding boxes [92, 344, 375]. Instead, it treats document understanding as a direct image-to-text translation task [92, 344, 375].
    > 
    > A **Swin Transformer** serves as the visual encoder [93, 344]. It splits the raw document image into patches and encodes them into high-dimensional visual embeddings [93, 344]. These embeddings are fed directly into a **BART text decoder** [93, 344]. You can prompt the decoder with a query like 'What is the total price?' and the model autoregressively generates the text [344].
    > 
    > During training, Donut uses a **Teacher-Forcing strategy**, calculating loss between input and ground-truth tokens [85]. Because numbers on an invoice or table do not have semantic sequence dependencies like natural sentences, the model learns directly from ground-truth transitions, generating structured JSON files that are immediately ready for database integration [85, 344]."

---

## 💎 Slide 11: State-of-the-Art: GLM-OCR (0.9B VLM) & Document Parsing
*   **Visual Representation:** Performance chart showcasing GLM-OCR scoring **94.62 on OmniDocBench V1.5** (ranking #1 overall) [388]. Below it, show a split screen showing: 1) Document Parsing (Formula extraction into LaTeX), and 2) Information Extraction (Invoice image to strict JSON schema) [393].
*   **Slayd Tezers (Slide Bullet Points):**
    *   **Z.ai GLM-OCR (2026):** A compact, state-of-the-art 0.9B parameter multimodal vision-language model [388]
    *   **Advanced Training:** Built on GLM-V, incorporating Multi-Token Prediction (MTP) loss and reinforcement learning [388]
    *   **Document Parsing Prompt:** Natively extracts text, complex tables, and scientific mathematical formulas using tags [393]
    *   **Information Extraction Prompt:** Evaluates document images and extracts structured key-value pairs directly into user-defined JSON schemas [393]
*   **Lecturer's Script (English):**
    > "Let's conclude today's lecture by looking at the absolute state-of-the-art in multimodal document intelligence: **GLM-OCR**, released recently in 2026 by the Z.ai research group [388]. 
    > 
    > At just 0.9 billion parameters, GLM-OCR is a compact but highly powerful VLM that ranks first overall on the OmniDocBench V1.5, scoring an incredible 94.62 [388]. It combines a **CogViT visual encoder**, a lightweight token downsampler, and a **GLM-0.5B language decoder** [388]. By introducing **Multi-Token Prediction (MTP) loss** and stable reinforcement learning, it achieves extreme accuracy with a very low computational and memory footprint [388, 389].
    > 
    > GLM-OCR natively supports two highly powerful prompt scenarios [393]. In **Document Parsing**, you can run standard text, formula, or table recognition [393]. It can take a scanned page of advanced calculus and convert it directly into formatted LaTeX equations. In **Information Extraction**, you provide the model with a strict, custom JSON schema, and it reads the document image and outputs perfectly formatted key-value pairs [393, 394]. This represents the absolute future of document AI, bridging the final gap between raw visual pixels and rich, structured semantic databases.
    > 
    > We will now take a 10-minute break. In our next period, we will open up our code editors and build our own custom Python OCR pipeline using OpenCV and Pytesseract. Please make sure your laptops are open and your Google Colab environments are ready. Thank you!"
