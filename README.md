# Lucy Edit - ComfyUI

<p align="center">
  <img src="assets/logo.png" width="680" alt="Lucy Edit Dev Logo"/>
</p>

<p align="center">
  🧪 <a href="http://github.com/DecartAI/lucy-edit-comfyui"><b>GitHub</b></a>
  &nbsp;|&nbsp; 🤗 <a href="https://huggingface.co/decart-ai/Lucy-Edit-Dev">Huggingface</a>
  &nbsp;|&nbsp; 📖 <a href="https://platform.decart.ai">Playground</a>
  &nbsp;|&nbsp; 📑 <a href="https://d2drjpuinn46lb.cloudfront.net/Lucy_Edit__High_Fidelity_Text_Guided_Video_Editing.pdf">Technical Report</a>
  &nbsp;|&nbsp; 💬 <a href="https://discord.gg/decart">Discord</a>
</p>

---

<img width="2559" height="812" alt="image" src="https://github.com/user-attachments/assets/291f41d2-f4a4-4d36-a0cf-f73a05fd0a0c" />


<div align="center">

<table>
<tr>
<td align="center">
  <video src="https://github.com/user-attachments/assets/5084db41-be23-47a2-97a2-4f6bf7229809" width="100%" controls>
    Your browser does not support the video tag.
  </video>
  <br/>
  <em>Put the woman in gothic black jeans and leather jacket and crop top under it.</em>
</td>
<td align="center">
  <video src="https://github.com/user-attachments/assets/f72e58e1-f00b-45a7-a2d4-28bea2aad11c" width="100%" controls>
    Your browser does not support the video tag.
  </video>
  <br/>
  <em>1.2) Put her in a clown outfit.</em>
</td>
<td align="center">
  <video src="https://github.com/user-attachments/assets/51263d11-66e9-4bdc-a41d-b59ee628332d" width="100%" controls>
    Your browser does not support the video tag.
  </video>
  <br/>
  <em>1.3) Put the woman in a red bikini with an open thick coat above it.</em>
</td>
</tr>
</table>
</div>


**Lucy Edit** is a **video editing** model that performs **instruction-guided edits** on videos using free-text prompts — it supports a variety of edits, such as **clothing & accessory changes**, **character changes**, **object insertions**, and **scene replacements** while preserving the motion and composition perfectly.

- 🏃‍♂️ **Motion Preservation** - preserves the motion and composition of videos perfectly, allowing precise edits.
- 🎯 **Edit reliability** — edits are more robust when compared to common inference time methods.
- 🧢 **Wardrobe & accessories** — change outfits, add glasses/earrings/hats/etc.
- 🧌 **Character Changes** — replace characters with monsters, animals and known characters. (e.g., "Replace the person with a polar bear")
- 🗺️ **Scenery swap** — move the scene (e.g., "transform the scene into a 2D cartoon,")  
- 📝 **Pure text instructions** — no finetuning, no masks required for common edits  

---

## 🛠️ Quickstart

### Installation

1. Clone this repo into custom_nodes folder.
1. Install dependencies: pip install -r requirements.txt

### Usage

1. Load the workflow from `examples/basic-api-lucy-edit.json`.
1. Get an api key from: https://platform.decart.ai/.

Please refer to the "Prompting Guidelines & Supported Edits" section for the best experience.

## 🎬 Demos

<div align="center">
### Sample 1
<table>
<tr>
<td align="center">
  <video src="https://github.com/user-attachments/assets/0ac94178-ce03-4e9d-9326-676fe6146bc6" width="100%" controls>
    Your browser does not support the video tag.
  </video>
  <br/>
  <em>1.1) Replace the man with an alien wearing the same leather jacket.</em>
</td>
<td align="center">
  <video src="https://github.com/user-attachments/assets/78275b81-04b4-4ee7-afa2-79fdcf54b688" width="100%" controls>
    Your browser does not support the video tag.
  </video>
  <br/>
  <em>1.2) Replace the man witha polar bear.</em>
</td>
<td align="center">
  <video src="https://github.com/user-attachments/assets/3ad89caa-8b89-4322-a1ef-e92df45c907a" width="100%" controls>
    Your browser does not support the video tag.
  </video>
  <br/>
  <em>1.3) Make it snow.</em>
</td>
</tr>
</table>

### Sample 2
<table>
<tr>
<td align="center">
  <video src="https://github.com/user-attachments/assets/443c36a8-dfc9-4a11-8873-4ed4985753ee" width="100%" controls>
    Your browser does not support the video tag.
  </video>
  <br/>
  <em>2.1) Replace the woman with Harley Quinn with full make up and a shirt with "Daddy's Lil Monster" written on it.</em>
</td>
<td align="center">
  <video src="https://github.com/user-attachments/assets/e9654e91-e0f4-479e-8632-d567178ea72f" width="100%" controls>
    Your browser does not support the video tag.
  </video>
  <br/>
  <em>2.2) Replace the girl with a lego character.</em>
</td>
<td align="center">
  <video src="https://github.com/user-attachments/assets/b58fcac9-2095-4686-9123-916250ccb9e3" width="100%" controls>
    Your browser does not support the video tag.
  </video>
  <br/>
  <em>2.3) Change the shit to a Manchester United jersey.</em>
</td>
</tr>
</table>

</div>

Note: The prompts above are not enriched, the model will react better to enriched prompts - as described in the prompt guideline section below.

---

## 🧭 Roadmap

* ✅ API based custom nodes.
* [ ] local inference custom nodes.

## 🔥 Latest News
- **[2025-09-17]**: Initial **Lucy Edit Dev** weights & reference code released.
- **[2025-09-16]**: Diffusers integration PR Merged. <a href="https://github.com/huggingface/diffusers/pull/12340">PR #12340</a>.
- **[2025-09-16]**: Diffusers integration PR opened. <a href="https://github.com/huggingface/diffusers/pull/12340">PR #12340</a>.


---

## Prompting Guidelines & Supported Edits

Lucy Edit is built for **precise, realistic, and identity-preserving video edits.**  
Prompts with ~20–30 descriptive words work best. Using the right **trigger words** helps the model understand your intent.  


### Trigger Words
- **Change** → Clothing or color modifications  
- **Add** → Adding animals or objects  
- **Replace** → Object substitution or subject swap  
- **Transform to** → Global scene or style transformations  


### Supported Edit Types

#### 1. Clothing Changes  
✅ **Best performance.** Lucy Edit excels at swapping outfits while preserving motion, pose, and identity.  
*Example*: *“Change the shirt to a kimono with wide sleeves and patterned fabric.”*  


#### 2. Human/Character Replacement  
✅ **Strong results.** Works well for transforming people into new characters or creatures. Detailed prompts are key.  
*Example*: *“Replace the person with a tiger, striped orange fur, muscular build, and glowing green eyes.”*  
*Example*: *“Replace the person with an 2D anime character, big eyes, blue gown and battle scars.”*  


#### 3. Replace Objects  
✅ **Reliable for structure-preserving swaps.** Ideal when replacing one object with another of similar scale.  
*Example*: *“Replace the apple with a glowing crystal ball emitting blue light.”*  


#### 4. Color Changes  
⚠️ **Mixed reliability.** Sometimes subtle, sometimes exaggerated. Works best with precise descriptions.  
*Example*: *“Change the jacket color to deep red leather with a glossy finish.”*  


#### 5. Add Objects  
⚠️ **Often attaches to the subject.** Works best for wearable or handheld props.  
*Example*: *“Add a golden crown on the person’s head, decorated with ornate jewels.”*  


#### 6. Global Transformations  
⚠️ **Effective for backgrounds or scene-wide changes, might alter the subject** Alter environment or style, might, Often changes the identity of the subject.
*Example*: *“Transform the sunny beach into a snowy tundra with falling snowflakes.”*  


### Additional Notes
- **Strengths:** Lucy Edit excels at **identity conservation, edit precision, realism, and prompt adherence.**  
- **Detail matters:** Longer prompts (20–30 words) describing style, appearance, and context improve results.  
- **Frame count:** 81-frame generations produce better temporal consistency than shorter clips.  
 
---

## 📬 Contact

* GitHub Issues: <a href="http://github.com/DecartAI/Lucy-Edit-ComfyUI">DecartAI/lucy-edit</a>.
* Discord: Join our discord server, <a href="https://discord.gg/decart">here</a>.
