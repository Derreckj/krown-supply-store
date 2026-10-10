from PIL import Image
import numpy as np

im = Image.open('public/images/products/krown-construction-jobsite-tumbler.png').convert('RGB')
arr = np.array(im, dtype=np.float32)

# Sample clean bottle rows
clean_top = arr[295:325, :, :] # 30 rows
clean_bot = arr[615:645, :, :] # 30 rows

mean_top = np.mean(clean_top, axis=0) # (1024, 3)
mean_bot = np.mean(clean_bot, axis=0) # (1024, 3)

np.random.seed(42)
for y in range(325, 615):
    t = (y - 325) / (615 - 325)
    row_est = (1.0 - t) * mean_top + t * mean_bot
    noise = np.random.normal(0, 1.2, size=(1024, 3))
    clean_row = np.clip(row_est + noise, 0, 255)
    
    # Apply to bottle pixels x: 335 to 665
    for x in range(335, 665):
        # Soft blend at the top and bottom borders (y: 325..335 and 605..615)
        # and side borders (x: 335..345 and 655..665)
        dist = min(x - 335, 665 - x, y - 325, 615 - y)
        w_blend = min(1.0, dist / 8.0)
        arr[y, x] = (1.0 - w_blend) * arr[y, x] + w_blend * clean_row[x]

clean_img = Image.fromarray(arr.astype(np.uint8), mode='RGB')
clean_img.save('test_clean_blank_bottle.jpg', quality=95)
print("Saved test_clean_blank_bottle.jpg")
