import os
import shutil
from PIL import Image

def deploy_perfect_axiom_hoodie():
    prod_dir = 'public/images/products'
    masters_dir = 'public/images/products/masters'

    os.makedirs(masters_dir, exist_ok=True)

    studio_img_path = 'test_axiom_hoodie_studio_definitive.jpg'
    if not os.path.exists(studio_img_path):
        raise FileNotFoundError(f"Missing {studio_img_path}")

    # Studio targets (Primary Mannequin / Studio display)
    studio_targets = [
        'axiom-heavyweight-hoodie-photoreal-v6.jpg',
        'axiom-heavyweight-hoodie-studio.jpg',
        'axiom-heavyweight-hoodie-v2.jpg',
        'axiom-heavyweight-hoodie-v3.jpg',
    ]

    for fname in studio_targets:
        dst = os.path.join(prod_dir, fname)
        dst_m = os.path.join(masters_dir, fname)
        shutil.copy2(studio_img_path, dst)
        shutil.copy2(studio_img_path, dst_m)
        print(f"Updated studio target: {dst} and master")

    # Model targets (Esports Studio Model Lookbook - zero crown)
    # The existing model-v6 is the high-tech gaming room model wearing the black hoodie with embroidered owl
    model_src = os.path.join(prod_dir, 'axiom-heavyweight-hoodie-model-v6.jpg')
    if os.path.exists(model_src):
        model_targets = [
            'axiom-heavyweight-hoodie-model.jpg',
            'axiom-heavyweight-hoodie-model-v2.jpg',
            'axiom-heavyweight-hoodie-model-v3.jpg',
            'axiom-heavyweight-hoodie-model-v4.jpg',
        ]
        for fname in model_targets:
            dst = os.path.join(prod_dir, fname)
            dst_m = os.path.join(masters_dir, fname)
            shutil.copy2(model_src, dst)
            shutil.copy2(model_src, dst_m)
            print(f"Updated model target: {dst} and master")

    print("\nSuccessfully deployed redesigned Axiom Heavyweight Hoodie across all catalog targets!")

if __name__ == '__main__':
    deploy_perfect_axiom_hoodie()
