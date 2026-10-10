import shutil
import os

brain_dir = r'C:\Users\derre\.gemini\antigravity-ide\brain\b0e8997a-a10d-435d-af7e-66fba7997fd7'
prod_dir = 'public/images/products'

src_studio = os.path.join(brain_dir, 'axiom_sweatshirt_studio_1791592277016.jpg')
src_model = os.path.join(brain_dir, 'axiom_sweatshirt_model_1791592297053.jpg')

dst_studio = os.path.join(prod_dir, 'axiom-crewneck-sweatshirt-studio.jpg')
dst_model = os.path.join(prod_dir, 'axiom-crewneck-sweatshirt-model.jpg')

shutil.copyfile(src_studio, dst_studio)
shutil.copyfile(src_model, dst_model)
print("Updated axiom-crewneck-sweatshirt-studio.jpg and model successfully!")
